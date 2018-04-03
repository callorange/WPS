FROM            archomai/overeats:bases
MAINTAINER      team.overeats@gmail.com

ENV             BUILD_MODE              production
ENV             DJANGO_SETTINGS_MODULE  config.settings.${BUILD_MODE}

# 소스폴더를 통째로 복사
COPY            . /srv/project

# nginx 설정파일을 복사 및 링크
RUN             cp -f /srv/project/.config/${BUILD_MODE}/nginx.conf         /etc/nginx/nginx.conf &&\
                cp -f /srv/project/.config/${BUILD_MODE}/nginx-app.conf     /etc/nginx/sites-available/ &&\
                rm -f /etc/nginx/sites-enabled/* &&\
                ln -sf /etc/nginx/sites-available/nginx-app.conf    /etc/nginx/sites-enabled/

# supervisor 설정파일을 복사
RUN             cp /srv/project/.config/${BUILD_MODE}/supervisord.conf      /etc/supervisor/conf.d/

# pkill nginx 후 supervisord 실행
CMD             pkill nginx; supervisord -n

EXPOSE          80