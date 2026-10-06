from __future__ import annotations

import os
from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import streamlit as st


ROOT = Path(__file__).resolve().parent
IGNORED_DIRECTORIES = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "__pycache__",
    ".ipynb_checkpoints",
}
IGNORED_FILES = {"secrets.toml", "credentials.json", "id_rsa", "id_ed25519"}
MAX_SEARCH_RESULTS = 20
MAX_PREVIEW_BYTES = 512 * 1024


def is_hidden_or_sensitive(name: str) -> bool:
    lowered_name = name.lower()
    return (
        name.startswith(".")
        or lowered_name in IGNORED_FILES
        or lowered_name.startswith(".env")
    )


def get_directory(relative_path: str) -> Path:
    candidate = (ROOT / relative_path).resolve()
    if candidate != ROOT and ROOT not in candidate.parents:
        raise ValueError("The requested location is outside the repository.")
    return candidate


def readable_size(size: int) -> str:
    value = float(size)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            return f"{value:.0f} {unit}" if unit == "B" else f"{value:.1f} {unit}"
        value /= 1024
    return f"{value:.1f} TB"


def visible_tree_entries(folder: Path):
    def record_error(error: OSError) -> None:
        raise error

    for current_root, directory_names, file_names in os.walk(
        folder, topdown=True, onerror=record_error, followlinks=False
    ):
        current_path = Path(current_root)
        directory_names[:] = sorted(
            name
            for name in directory_names
            if name.lower() not in IGNORED_DIRECTORIES
            and not is_hidden_or_sensitive(name)
            and not (current_path / name).is_symlink()
        )
        for name in file_names:
            file_path = current_path / name
            if not is_hidden_or_sensitive(name) and not file_path.is_symlink():
                yield file_path


def create_folder_archive(relative_path: str) -> bytes:
    folder = get_directory(relative_path)
    if not folder.is_dir():
        raise ValueError("The selected folder is no longer available.")

    archive_buffer = BytesIO()
    archive_root = Path(relative_path).name or "repository"
    with ZipFile(archive_buffer, mode="w", compression=ZIP_DEFLATED) as archive:
        for file_path in visible_tree_entries(folder):
            archive_name = Path(archive_root) / file_path.relative_to(folder)
            archive.write(file_path, archive_name.as_posix())
    return archive_buffer.getvalue()


def prepare_download(path: str, is_directory: bool) -> None:
    st.session_state.download_target = (path, is_directory)


def prepare_open(path: str, is_directory: bool) -> None:
    if is_directory:
        st.session_state.current_directory = path
        st.session_state.selected_file = ""
    else:
        parent = Path(path).parent.as_posix()
        st.session_state.current_directory = "" if parent == "." else parent
        st.session_state.selected_file = path
    st.session_state.download_target = None


def select_search_item(path: str, is_directory: bool) -> None:
    st.session_state.selected_search_item = (path, is_directory)
    st.session_state.download_target = None


def clear_search_selection() -> None:
    st.session_state.selected_search_item = None


def render_file_preview(relative_path: str) -> None:
    file_path = get_directory(relative_path)
    if not file_path.is_file():
        st.error("This file is no longer available.")
        return

    file_size = file_path.stat().st_size
    st.subheader(f"📄 {file_path.name}")
    st.caption(f"`{relative_path}` · {readable_size(file_size)}")
    if file_size <= MAX_PREVIEW_BYTES:
        file_bytes = file_path.read_bytes()
        if file_path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp"}:
            st.image(file_bytes)
        else:
            try:
                text_content = file_bytes.decode("utf-8")
            except UnicodeDecodeError:
                st.info("This file is binary and cannot be previewed here.")
            else:
                st.code(text_content, language=file_path.suffix.lstrip(".") or None)
    else:
        st.info("This file is too large to preview. Use its Download button.")


@st.cache_data(ttl=300, show_spinner=False)
def build_search_index(root: str) -> tuple[list[tuple[str, str, bool]], list[str]]:
    entries: list[tuple[str, str, bool]] = []
    errors: list[str] = []
    root_path = Path(root)

    def record_error(error: OSError) -> None:
        errors.append(str(error))

    for current_root, directory_names, file_names in os.walk(
        root_path, topdown=True, onerror=record_error, followlinks=False
    ):
        current_path = Path(current_root)
        directory_names[:] = sorted(
            name
            for name in directory_names
            if name.lower() not in IGNORED_DIRECTORIES
            and not is_hidden_or_sensitive(name)
            and not (current_path / name).is_symlink()
        )

        for name in directory_names:
            path = (current_path / name).relative_to(root_path).as_posix()
            entries.append((name, path, True))
        for name in file_names:
            if is_hidden_or_sensitive(name) or (current_path / name).is_symlink():
                continue
            path = (current_path / name).relative_to(root_path).as_posix()
            entries.append((name, path, False))

    return entries, errors


def go_to(path: str) -> None:
    st.session_state.current_directory = path
    st.session_state.selected_file = ""


st.set_page_config(
    page_title="Repository Explorer",
    page_icon="📁",
    layout="wide",
)

st.title("📁 Repository Explorer")
st.caption("Browse files and folders in the repository deployed with this app.")
st.info(
    "Downloads are saved by your browser, usually in its **Downloads** folder. "
    "Press **Ctrl+J** on Windows/Linux, or open **Downloads** from your browser menu."
)

if "current_directory" not in st.session_state:
    st.session_state.current_directory = ""
if "selected_file" not in st.session_state:
    st.session_state.selected_file = ""
if "download_target" not in st.session_state:
    st.session_state.download_target = None
if "selected_search_item" not in st.session_state:
    st.session_state.selected_search_item = None

query = st.text_input(
    "Search files and folders",
    placeholder="Type a file or folder name...",
    help="Search all visible repository files and folders by name.",
    on_change=clear_search_selection,
)

search_mode = bool(query.strip())
selected_search_item = st.session_state.selected_search_item

if search_mode and selected_search_item is None:
    search_entries, search_errors = build_search_index(str(ROOT))
    normalized_query = query.strip().casefold()
    matches = [
        entry for entry in search_entries if normalized_query in entry[0].casefold()
    ]
    matches.sort(
        key=lambda entry: (
            entry[0].casefold() != normalized_query,
            not entry[2],
            entry[0].casefold(),
            entry[1].casefold(),
        )
    )

    with st.container(border=True):
        if matches:
            st.caption(
                f"Showing {min(len(matches), MAX_SEARCH_RESULTS)} of "
                f"{len(matches)} matching names"
            )
            for index, (name, path, is_directory) in enumerate(
                matches[:MAX_SEARCH_RESULTS]
            ):
                result_columns = st.columns([0.78, 0.22])
                icon = "📁" if is_directory else "📄"
                result_columns[0].button(
                    f"{icon}  {name}  ·  {path}",
                    key=f"search_result_{index}_{path}",
                    use_container_width=True,
                    on_click=select_search_item,
                    args=(path, is_directory),
                )
                if result_columns[1].button(
                    "Prepare download",
                    key=f"search_download_{index}_{path}",
                    use_container_width=True,
                    on_click=prepare_download,
                    args=(path, is_directory),
                ):
                    st.rerun()
        else:
            st.info("No matching file or folder name was found.")

    if search_errors:
        with st.expander("Some locations could not be searched"):
            for error in search_errors:
                st.error(error)

if search_mode and selected_search_item is not None:
    selected_path, selected_is_directory = selected_search_item
    with st.container(border=True):
        if st.button("← Back to search results", key="back_to_search_results"):
            st.session_state.selected_search_item = None
            st.session_state.download_target = None
            st.rerun()

        try:
            selected_fs_path = get_directory(selected_path)
            if selected_is_directory:
                if not selected_fs_path.is_dir():
                    st.error("This folder is no longer available.")
                else:
                    st.markdown(f"**Folder:** `/{selected_path}`")
                    if st.button(
                        f"Prepare download: {selected_fs_path.name or 'repository'}.zip",
                        key=f"search_selected_folder_download_{selected_path}",
                        on_click=prepare_download,
                        args=(selected_path, True),
                    ):
                        st.rerun()
                    folder_children = sorted(
                        (
                            entry
                            for entry in selected_fs_path.iterdir()
                            if not entry.is_symlink()
                            and not is_hidden_or_sensitive(entry.name)
                            and not (
                                entry.is_dir()
                                and entry.name.lower() in IGNORED_DIRECTORIES
                            )
                        ),
                        key=lambda entry: (
                            not entry.is_dir(),
                            entry.name.casefold(),
                        ),
                    )
                    if not folder_children:
                        st.info("This folder is empty or has no visible items.")
                    for index, child in enumerate(folder_children):
                        child_path = child.relative_to(ROOT).as_posix()
                        child_is_directory = child.is_dir()
                        child_columns = st.columns([0.1, 0.56, 0.17, 0.17])
                        child_columns[0].write("📁" if child_is_directory else "📄")
                        child_columns[1].write(f"**{child.name}**")
                        child_columns[2].button(
                            "Open",
                            key=f"search_folder_child_{index}_{child_path}",
                            on_click=select_search_item,
                            args=(child_path, child_is_directory),
                        )
                        child_columns[3].button(
                            "Prepare download",
                            key=f"search_folder_child_download_{index}_{child_path}",
                            on_click=prepare_download,
                            args=(child_path, child_is_directory),
                        )
            else:
                render_file_preview(selected_path)
                if selected_fs_path.is_file():
                    if st.download_button(
                        f"⬇️ Download {selected_fs_path.name}",
                        data=selected_fs_path.read_bytes(),
                        file_name=selected_fs_path.name,
                        mime="application/octet-stream",
                        key=f"search_selected_file_download_{selected_path}",
                    ):
                        st.success(
                            "Download started. Find the file in your browser's "
                            "Downloads list (Ctrl+J on Windows/Linux)."
                        )
        except (OSError, ValueError) as error:
            st.error(f"Could not open this item: {error}")

download_target = st.session_state.download_target
if download_target:
    download_path, download_is_directory = download_target
    try:
        if download_is_directory:
            download_bytes = create_folder_archive(download_path)
            download_name = f"{Path(download_path).name or 'repository'}.zip"
            download_mime = "application/zip"
        else:
            target_file = get_directory(download_path)
            if not target_file.is_file():
                raise ValueError("The selected file is no longer available.")
            download_bytes = target_file.read_bytes()
            download_name = target_file.name
            download_mime = "application/octet-stream"

        st.success(f"Ready: **{download_name}**. Click below to save it to your device.")
        if st.download_button(
            f"⬇️ Click to download {download_name}",
            data=download_bytes,
            file_name=download_name,
            mime=download_mime,
            key=f"download_ready_{download_path}",
        ):
            st.success(
                "Download started. Find the file in your browser's Downloads "
                "list (Ctrl+J on Windows/Linux)."
            )
    except (OSError, ValueError) as error:
        st.error(f"Could not prepare this download: {error}")

if not search_mode:
    st.divider()

    current_directory = st.session_state.current_directory
    try:
        current_path = get_directory(current_directory)
        if not current_path.is_dir():
            st.error("This folder is no longer available.")
            go_to("")
            current_path = ROOT
            current_directory = ""
        children = sorted(
            (
                entry
                for entry in current_path.iterdir()
                if not is_hidden_or_sensitive(entry.name)
                and not entry.is_symlink()
                and not (
                    entry.is_dir()
                    and entry.name.lower() in IGNORED_DIRECTORIES
                )
            ),
            key=lambda entry: (not entry.is_dir(), entry.name.casefold()),
        )
    except (OSError, ValueError) as error:
        st.error(f"Could not open this folder: {error}")
        children = []

    if current_directory:
        parent = Path(current_directory).parent.as_posix()
        if parent == ".":
            parent = ""
        if st.button("← Up one folder", key="up_one_folder"):
            go_to(parent)
            st.rerun()

    location = f"/{current_directory}" if current_directory else "/"
    st.markdown(f"**Location:** `{location}`")

    if not children:
        st.info("This folder is empty or has no visible items.")
    else:
        for index, entry in enumerate(children):
            columns = st.columns([0.08, 0.66, 0.16, 0.1])
            is_directory = entry.is_dir()
            relative_path = entry.relative_to(ROOT).as_posix()
            columns[0].write("📁" if is_directory else "📄")
            columns[1].write(f"**{entry.name}**")
            if is_directory:
                columns[2].write("Folder")
                if columns[3].button("Open", key=f"open_{index}_{relative_path}"):
                    prepare_open(relative_path, True)
                    st.rerun()
                if st.button(
                    f"Prepare download: {entry.name}.zip",
                    key=f"download_folder_{index}_{relative_path}",
                    on_click=prepare_download,
                    args=(relative_path, True),
                ):
                    st.rerun()
            else:
                try:
                    columns[2].write(readable_size(entry.stat().st_size))
                except OSError as error:
                    columns[2].error(f"Unavailable: {error}")
                if columns[3].button("Details", key=f"details_{index}_{relative_path}"):
                    st.session_state.selected_file = relative_path
                    st.session_state.download_target = None
                if st.button(
                    f"Prepare download: {entry.name}",
                    key=f"download_file_{index}_{relative_path}",
                    on_click=prepare_download,
                    args=(relative_path, False),
                ):
                    st.rerun()

selected_file = st.session_state.selected_file
if selected_file and not search_mode:
    try:
        render_file_preview(selected_file)
    except (OSError, ValueError) as error:
        st.error(f"Could not read file details: {error}")
