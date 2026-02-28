import streamlit as st
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from streamlit_drawable_canvas import st_canvas
import streamlit as st
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from streamlit_drawable_canvas import st_canvas
import streamlit as st
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from streamlit_drawable_canvas import st_canvas
import streamlit as st
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from streamlit_drawable_canvas import st_canvas

def app():
    # Load model
    model = load_model("mnist_ann_model.h5")

    st.title("MNIST Digit Recognizer")
    st.markdown("🖊️ Draw a digit below and click Submit to predict.")

    # Canvas for drawing
    canvas_result = st_canvas(
        fill_color="black",
        stroke_width=10,
        stroke_color="white",
        background_color="black",
        height=280,
        width=280,
        drawing_mode="freedraw",
        key="canvas",
    )

    # Add a Submit button
    if st.button("Submit"):
        if canvas_result is not None and hasattr(canvas_result, "image_data"):
            image_data = canvas_result.image_data

            if image_data is not None:
                try:
                    # Preprocess
                    img = image_data.astype("uint8")
                    img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
                    img = cv2.resize(img, (28, 28))
                    img = cv2.bitwise_not(img)
                    img = img.astype("float32") / 255.0
                    img = img.reshape(1, 784)

                    # Predict
                    pred = model.predict(img)
                    pred_class = np.argmax(pred)

                    st.subheader(f"✅ Predicted Digit: {pred_class}")
                except Exception as e:
                    st.error(f"⚠️ Error during prediction: {e}")
            else:
                st.warning("⚠️ Please draw a digit before submitting.")
        else:
            st.warning("⚠️ Canvas is not ready yet.")

app()