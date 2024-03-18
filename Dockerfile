FROM archlinux:latest
RUN pacman -Syu --noconfirm git python && \
pacman -Sc --noconfirm && \
useradd --create-home appuser
WORKDIR /home/appuser/app
COPY . .
RUN chown -R appuser:appuser /home/appuser/app
USER appuser
RUN python -m venv /home/appuser/venv && \
/home/appuser/venv/bin/pip install -U pip && \
/home/appuser/venv/bin/pip install -r requirements.txt && \
/home/appuser/venv/bin/pip cache purge
RUN PATH="/home/appuser/venv/bin:$PATH" ./build.sh
EXPOSE 8080
CMD [ "/home/appuser/venv/bin/python", "main.py" ]
