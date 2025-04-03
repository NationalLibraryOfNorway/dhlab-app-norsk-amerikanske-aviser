FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
        ENV PORT=8501
        EXPOSE $PORT
        WORKDIR /main_amerika.py

        COPY requirements.txt ./requirements.txt
        RUN uv pip install          \
            -r requirements.txt     \
            --system                \
            --compile-bytecode

        # Warm up caches
        RUN python -c 'import streamlit, dhlab, pandas'
        RUN timeout 5s streamlit hello; exit 0

        COPY ./NB-logo-no-eng-svart.png ./main_amerika.py ./norske_aviser.csv ./
        COPY ./pages ./pages

        CMD streamlit run main_amerika.py                   \
            --server.port ${PORT}                           \
            --server.baseUrlPath /norsk-amerikanske-aviser  \
            --browser.gatherUsageStats false

