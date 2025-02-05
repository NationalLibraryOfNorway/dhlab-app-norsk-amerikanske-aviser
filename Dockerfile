FROM python:3.12
        ENV PORT=8501
        EXPOSE $PORT
        WORKDIR /main_amerika.py
        COPY requirements.txt ./requirements.txt
        RUN pip3 install -r requirements.txt
        COPY . .
        CMD streamlit run main_amerika.py --server.port ${PORT} --server.baseUrlPath /norsk-amerikanske-aviser

