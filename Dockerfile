FROM python:3.11-alpine
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
RUN chown -R appuser:appgroup /app
EXPOSE 8080
USER appuser
CMD [ "python", "main.py" ]
