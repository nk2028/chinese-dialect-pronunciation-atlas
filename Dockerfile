FROM archlinux:latest
RUN pacman -Syu --noconfirm git python python-pip && \
pacman -Sc --noconfirm && \
useradd --create-home appuser
WORKDIR /home/appuser/app
COPY . .
RUN chown -R appuser:appuser /home/appuser/app
USER appuser
RUN pip install -r requirements.txt
RUN ./build.sh
EXPOSE 8080
CMD [ "python", "main.py" ]
