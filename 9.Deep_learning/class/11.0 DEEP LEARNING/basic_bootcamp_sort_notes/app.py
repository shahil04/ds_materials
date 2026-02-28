#!/usr/bin/env python
"""
Streamlit App: Interactive MNIST ANN Playground

Features:
- Load & preview MNIST data
- Build configurable ANN with:
    - Hidden layers, units, activation
    - Optimizer, learning rate, loss
    - Dropout, L2 regularization
    - Callbacks (EarlyStopping, ReduceLROnPlateau)
- Train and visualize:
    - Loss & accuracy curves
    - Test accuracy
    - Sample predictions
- Manual hyperparameter search (grid over LR & batch size)
- Optional Optuna hyperparameter tuning (if optuna is installed)
"""

import os
import numpy as np
import matplotlib.pyplot as plt

import streamlit as st

import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import regularizers
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ReduceLROnPlateau,
)

st.set_page_config(page_title="MNIST ANN Playground", layout="wide")

# -----------------------------
# 1. Load & cache dataset
# -----------------------------
@st.cache_resource
def load_mnist(subsample_train=20000, subsample_test=5000):
    (X_train, y_train), (X_test, y_test) = mnist.load_data()

    # Flatten & normalize
    X_train = X_train.reshape(-1, 28 * 28).astype("float32") / 255.0
    X_test = X_test.reshape(-1, 28 * 28).astype("float32") / 255.0

    num_classes = len(np.unique(y_train))
    y_train_cat = to_categorical(y_train, num_classes)
    y_test_cat = to_categorical(y_test, num_classes)

    # Subsample for faster demos
    if subsample_train is not None and subsample_train < X_train.shape[0]:
        X_train = X_train[:subsample_train]
        y_train_cat = y_train_cat[:subsample_train]
        y_train = y_train[:subsample_train]

    if subsample_test is not None and subsample_test < X_test.shape[0]:
        X_test = X_test[:subsample_test]
        y_test_cat = y_test_cat[:subsample_test]
        y_test = y_test[:subsample_test]

    return (X_train, y_train, y_train_cat), (X_test, y_test, y_test_cat), num_classes


# -----------------------------
# 2. Helper: build model
# -----------------------------
def build_ann_model(
    input_dim: int,
    num_classes: int,
    n_hidden: int,
    units: int,
    hidden_activation: str,
    output_activation: str,
    l2_lambda: float,
    dropout_rate: float,
    optimizer_name: str,
    learning_rate: float,
    loss_name: str,
):
    model = Sequential()

    # First hidden layer with input shape
    model.add(
        Dense(
            units,
            activation=hidden_activation,
            input_shape=(input_dim,),
            kernel_regularizer=regularizers.l2(l2_lambda) if l2_lambda > 0 else None,
        )
    )
    if dropout_rate > 0:
        model.add(Dropout(dropout_rate))

    # Additional hidden layers
    for _ in range(n_hidden - 1):
        model.add(
            Dense(
                units,
                activation=hidden_activation,
                kernel_regularizer=regularizers.l2(l2_lambda) if l2_lambda > 0 else None,
            )
        )
        if dropout_rate > 0:
            model.add(Dropout(dropout_rate))

    # Output layer
    model.add(Dense(num_classes, activation=output_activation))

    # Optimizer
    optimizer_name = optimizer_name.lower()
    if optimizer_name == "sgd":
        optimizer = tf.keras.optimizers.SGD(learning_rate=learning_rate)
    elif optimizer_name == "rmsprop":
        optimizer = tf.keras.optimizers.RMSprop(learning_rate=learning_rate)
    else:
        optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

    model.compile(optimizer=optimizer, loss=loss_name, metrics=["accuracy"])
    return model


# -----------------------------
# 3. Helper: plot history
# -----------------------------
def plot_history(history, title_prefix="Model"):
    hist = history.history
    epochs = range(1, len(hist.get("loss", [])) + 1)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # Loss
    axes[0].plot(epochs, hist.get("loss", []), label="Train Loss")
    if "val_loss" in hist:
        axes[0].plot(epochs, hist["val_loss"], label="Val Loss")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Loss")
    axes[0].set_title(f"{title_prefix} - Loss")
    axes[0].legend()

    # Accuracy
    if "accuracy" in hist:
        axes[1].plot(epochs, hist["accuracy"], label="Train Acc")
    if "val_accuracy" in hist:
        axes[1].plot(epochs, hist["val_accuracy"], label="Val Acc")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Accuracy")
    axes[1].set_title(f"{title_prefix} - Accuracy")
    axes[1].legend()

    plt.tight_layout()
    return fig


# -----------------------------
# 4. Load data once
# -----------------------------
(X_train, y_train, y_train_cat), (X_test, y_test, y_test_cat), NUM_CLASSES = load_mnist()

# -----------------------------
# UI Layout
# -----------------------------
st.title("🧠 MNIST ANN Interactive Playground (Keras + Callbacks + Tuning)")

tabs = st.tabs(["📊 Data Preview", "🧩 Single Model Training", "📈 Hyperparameter Search", "🧪 Optuna (Advanced)"])

# =============================
# TAB 1: Data Preview
# =============================
with tabs[0]:
    st.header("📊 Data Preview")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Sample Images")
        n_show = st.slider("Number of images to show", 4, 16, 9)
        fig, axes = plt.subplots(1, n_show, figsize=(n_show * 1.2, 1.5))
        for i in range(n_show):
            axes[i].imshow(X_train[i].reshape(28, 28), cmap="gray")
            axes[i].axis("off")
            axes[i].set_title(int(y_train[i]))
        st.pyplot(fig)

    with col2:
        st.write("### Dataset Shapes")
        st.write(f"Train X: {X_train.shape}")
        st.write(f"Train y (one-hot): {y_train_cat.shape}")
        st.write(f"Test X: {X_test.shape}")
        st.write(f"Test y (one-hot): {y_test_cat.shape}")
        st.info(
            "We are using a **subsampled** MNIST (by default) to keep training "
            "fast for classroom demos."
        )


# =============================
# TAB 2: Single Model Training
# =============================
with tabs[1]:
    st.header("🧩 Build & Train a Custom ANN")

    with st.sidebar:
        st.subheader("🔧 Model Hyperparameters")

        n_hidden = st.slider("Number of hidden layers", 1, 3, 2)
        units = st.slider("Units per hidden layer", 32, 512, 256, step=32)

        hidden_activation = st.selectbox("Hidden activation", ["relu", "tanh", "sigmoid"])
        output_activation = "softmax"

        optimizer_name = st.selectbox("Optimizer", ["adam", "sgd", "rmsprop"])
        learning_rate = st.select_slider(
            "Learning rate",
            options=[1e-1, 5e-2, 1e-2, 5e-3, 1e-3, 5e-4, 1e-4],
            value=1e-3,
            format_func=lambda x: f"{x:.0e}",
        )

        loss_name = "categorical_crossentropy"

        st.subheader("🛡 Regularization")
        l2_lambda = st.select_slider(
            "L2 regularization (lambda)", options=[0.0, 1e-5, 1e-4, 1e-3, 1e-2], value=1e-4
        )
        dropout_rate = st.slider("Dropout rate", 0.0, 0.7, 0.3, step=0.1)

        st.subheader("⚙ Training Settings")
        epochs = st.slider("Epochs", 1, 30, 10)
        batch_size = st.selectbox("Batch size", [32, 64, 128, 256], index=2)
        val_split = st.slider("Validation split", 0.05, 0.3, 0.1, step=0.05)

        st.subheader("⏱ Callbacks")
        use_early_stopping = st.checkbox("Use EarlyStopping", value=True)
        es_patience = st.slider("EarlyStopping patience", 2, 10, 5) if use_early_stopping else None

        use_reduce_lr = st.checkbox("Use ReduceLROnPlateau", value=True)
        rlrop_patience = st.slider("ReduceLROnPlateau patience", 2, 10, 3) if use_reduce_lr else None

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.write("### 1️⃣ Configure and Train Model")

        if st.button("🚀 Train Model", type="primary"):
            st.write("Building model...")
            model = build_ann_model(
                input_dim=28 * 28,
                num_classes=NUM_CLASSES,
                n_hidden=n_hidden,
                units=units,
                hidden_activation=hidden_activation,
                output_activation=output_activation,
                l2_lambda=l2_lambda,
                dropout_rate=dropout_rate,
                optimizer_name=optimizer_name,
                learning_rate=learning_rate,
                loss_name=loss_name,
            )

            callbacks = []
            if use_early_stopping:
                callbacks.append(
                    EarlyStopping(
                        monitor="val_loss",
                        patience=es_patience,
                        restore_best_weights=True,
                        verbose=1,
                    )
                )
            if use_reduce_lr:
                callbacks.append(
                    ReduceLROnPlateau(
                        monitor="val_loss",
                        patience=rlrop_patience,
                        factor=0.5,
                        min_lr=1e-6,
                        verbose=1,
                    )
                )

            st.write("Training...")
            with st.spinner("Training the model..."):
                history = model.fit(
                    X_train,
                    y_train_cat,
                    epochs=epochs,
                    batch_size=batch_size,
                    validation_split=val_split,
                    verbose=0,
                    callbacks=callbacks,
                )

            st.success("Training finished!")

            st.write("### 2️⃣ Training Curves")
            fig_hist = plot_history(history, title_prefix="Custom ANN")
            st.pyplot(fig_hist)

            st.write("### 3️⃣ Evaluate on Test Set")
            test_loss, test_acc = model.evaluate(X_test, y_test_cat, verbose=0)
            st.metric("Test Accuracy", f"{test_acc:.4f}")
            st.metric("Test Loss", f"{test_loss:.4f}")

            st.write("### 4️⃣ Sample Predictions")
            n_preds = 12
            preds = model.predict(X_test[:n_preds])
            y_pred = np.argmax(preds, axis=1)

            fig, axes = plt.subplots(2, n_preds // 2, figsize=(n_preds * 0.8, 3))
            axes = axes.ravel()
            for i in range(n_preds):
                axes[i].imshow(X_test[i].reshape(28, 28), cmap="gray")
                axes[i].axis("off")
                axes[i].set_title(f"P:{y_pred[i]} / T:{y_test[i]}")
            plt.tight_layout()
            st.pyplot(fig)

    with col_right:
        st.write("### Current Configuration (for teaching)")
        st.json(
            {
                "Hidden layers": n_hidden,
                "Units per layer": units,
                "Hidden activation": hidden_activation,
                "Output activation": output_activation,
                "Optimizer": optimizer_name,
                "Learning rate": learning_rate,
                "Loss": loss_name,
                "L2 λ": l2_lambda,
                "Dropout": dropout_rate,
                "Epochs": epochs,
                "Batch size": batch_size,
                "Val split": val_split,
                "EarlyStopping": use_early_stopping,
                "ReduceLROnPlateau": use_reduce_lr,
            }
        )


# =============================
# TAB 3: Manual Hyperparameter Search
# =============================
with tabs[2]:
    st.header("📈 Manual Hyperparameter Search (Mini Grid Search)")

    st.write(
        "This section runs a **small grid search** over learning rates and batch sizes. "
        "Useful for showing students how hyperparameters affect validation accuracy."
    )

    lrs = st.multiselect(
        "Choose learning rates",
        options=[1e-1, 5e-2, 1e-2, 5e-3, 1e-3, 5e-4],
        default=[1e-2, 1e-3],
        format_func=lambda x: f"{x:.0e}",
    )
    bss = st.multiselect("Choose batch sizes", options=[32, 64, 128, 256], default=[64, 128])

    gs_epochs = st.slider("Epochs per combination", 1, 10, 3)
    gs_val_split = st.slider("Validation split", 0.05, 0.3, 0.1, step=0.05)

    if st.button("🔍 Run Manual Grid Search"):
        results = []
        progress = st.progress(0)
        total = max(len(lrs) * len(bss), 1)
        done = 0

        st.write("Running grid search...")
        for lr in lrs:
            for bs in bss:
                done += 1
                progress.progress(done / total)
                st.write(f"Training with lr={lr:.0e}, batch_size={bs}...")

                model = build_ann_model(
                    input_dim=28 * 28,
                    num_classes=NUM_CLASSES,
                    n_hidden=2,
                    units=128,
                    hidden_activation="relu",
                    output_activation="softmax",
                    l2_lambda=0.0,
                    dropout_rate=0.0,
                    optimizer_name="adam",
                    learning_rate=lr,
                    loss_name="categorical_crossentropy",
                )

                history = model.fit(
                    X_train,
                    y_train_cat,
                    epochs=gs_epochs,
                    batch_size=bs,
                    validation_split=gs_val_split,
                    verbose=0,
                )
                val_acc = history.history["val_accuracy"][-1]
                results.append({"lr": lr, "batch_size": bs, "val_accuracy": float(val_acc)})

        st.success("Grid search complete!")
        st.write("### Results Table")
        st.table(results)

        # Simple bar plot
        labels = [f"lr={r['lr']:.0e}, bs={r['batch_size']}" for r in results]
        vals = [r["val_accuracy"] for r in results]

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.barh(labels, vals)
        ax.set_xlabel("Validation Accuracy")
        ax.set_title("Manual Hyperparameter Search Results")
        st.pyplot(fig)


# =============================
# TAB 4: Optuna (Advanced)
# =============================
with tabs[3]:
    st.header("🧪 Optuna Hyperparameter Optimization (Advanced)")

    st.write(
        "This section uses **Optuna** to automatically search for good hyperparameters.\n"
        "If Optuna is not installed, install it with:\n"
        "```bash\n"
        "!pip install optuna -q\n"
        "```"
    )

    try:
        import optuna  # type: ignore

        optuna_available = True
        st.success(f"Optuna available (version: {optuna.__version__})")
    except Exception:
        optuna_available = False
        st.error("Optuna is NOT installed. Install it in your environment to use this tab.")

    if optuna_available:
        n_trials = st.slider("Number of Optuna trials", 1, 20, 5)
        opt_epochs = st.slider("Epochs per trial", 1, 10, 5)
        opt_val_split = st.slider("Validation split", 0.05, 0.3, 0.1, step=0.05)

        def create_optuna_model(trial):
            model = Sequential()
            # Number of hidden layers: 1–3
            n_hidden = trial.suggest_int("n_hidden", 1, 3)
            for i in range(n_hidden):
                units = trial.suggest_int(f"units_{i}", 64, 512, step=64)
                if i == 0:
                    model.add(Dense(units, activation="relu", input_shape=(28 * 28,)))
                else:
                    model.add(Dense(units, activation="relu"))
                dr = trial.suggest_float(f"dropout_{i}", 0.0, 0.5, step=0.1)
                if dr > 0:
                    model.add(Dropout(dr))

            model.add(Dense(NUM_CLASSES, activation="softmax"))
            lr = trial.suggest_float("learning_rate", 1e-4, 1e-2, log=True)
            opt = tf.keras.optimizers.Adam(learning_rate=lr)
            model.compile(optimizer=opt, loss="categorical_crossentropy", metrics=["accuracy"])
            return model

        def optuna_objective(trial):
            model = create_optuna_model(trial)
            batch_size = trial.suggest_categorical("batch_size", [64, 128, 256])
            history = model.fit(
                X_train,
                y_train_cat,
                validation_split=opt_val_split,
                epochs=opt_epochs,
                batch_size=batch_size,
                verbose=0,
            )
            return history.history["val_accuracy"][-1]

        if st.button("🚀 Run Optuna Search"):
            with st.spinner("Running Optuna study..."):
                study = optuna.create_study(direction="maximize")
                study.optimize(optuna_objective, n_trials=n_trials, show_progress_bar=False)

            best_trial = study.best_trial
            st.success("Optuna search completed!")
            st.write("### Best Trial")
            st.write(f"Best validation accuracy: **{best_trial.value:.4f}**")
            st.json(best_trial.params)

            # Rebuild and train best model a bit more
            st.write("### Train Best Model on Train/Val and Evaluate on Test")

            class SimpleTrial:
                def __init__(self, params):
                    self.params = params

                def suggest_int(self, name, low, high, step=1):
                    return self.params[name]

                def suggest_float(self, name, low, high, step=None, log=False):
                    return self.params[name]

                def suggest_categorical(self, name, choices):
                    return self.params[name]

            dummy_trial = SimpleTrial(best_trial.params)
            best_model = create_optuna_model(dummy_trial)
            best_bs = best_trial.params.get("batch_size", 128)

            history = best_model.fit(
                X_train,
                y_train_cat,
                validation_split=opt_val_split,
                epochs=opt_epochs,
                batch_size=best_bs,
                verbose=0,
            )

            test_loss, test_acc = best_model.evaluate(X_test, y_test_cat, verbose=0)
            st.metric("Best Optuna Model - Test Accuracy", f"{test_acc:.4f}")
            st.metric("Best Optuna Model - Test Loss", f"{test_loss:.4f}")

            fig_hist = plot_history(history, title_prefix="Optuna Best Model")
            st.pyplot(fig_hist)

            st.write("### Sample Predictions from Optuna-Tuned Model")
            preds = best_model.predict(X_test[:10])
            y_pred = np.argmax(preds, axis=1)

            fig, axes = plt.subplots(2, 5, figsize=(10, 4))
            axes = axes.ravel()
            for i in range(10):
                axes[i].imshow(X_test[i].reshape(28, 28), cmap="gray")
                axes[i].axis("off")
                axes[i].set_title(f"P:{y_pred[i]} / T:{y_test[i]}")
            plt.tight_layout()
            st.pyplot(fig)
