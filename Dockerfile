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
        RUN timeout 5s streamlit run main_amerika.py; exit 0
        RUN python -c 'import dhlab, pandas'

        COPY ./NB-logo-no-eng-svart.png ./main_amerika.py ./norske_aviser.csv ./
        COPY ./pages ./pages

        CMD streamlit run main_amerika.py                   \
            --server.port ${PORT}                           \
            --server.baseUrlPath /norsk-amerikanske-aviser  \
            --browser.gatherUsageStats false

