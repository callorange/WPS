
# OverEats

URL : www.overeats.kr

Elastic Beanstalk에 Nginx-uWSGI-Django로 구성된 Docker 이미지를 배포합니다.

## Requirements

### 공통사항

- Python (3.6)
- .secrets/의 JSON파일 작성 (아래의 .secrets항목 참조)
- Docker설치 필요

#### GeoDjango 설정
식당 위치기반 검색에 Geometry를 사용하므로 사용하는 시스템에 따라 필요 라이브러리 추가 설치가 되야함.  
[GeoDjango Document 보기](https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/#geodjango-installation)

1. 필요 라이브러리 설치
    1. 필요 라이브러리 참조
        - [GeoDjango - Spatial database](https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/#spatial-database)
    2. mac - homebrew
        - [GeoDjango Document - Mac, Homebrew](https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/#homebrew)
          ```bash
          $ brew install gdal
          $ brew install libgeoip
          ```
    3. ubuntu
        - [GeoDjango Document - linux](https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/geolibs/#installing-geospatial-libraries)
          ```bash
          $ sudo apt-get install binutils libproj-dev gdal-bin
          ```
2. DB설정
    1. PostgreSQL
        - [GeoDjango - postgis](https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/postgis/)
        - test 코드를 실행 하려면 접속 계정이 superuser 권한이 있어야 합니다. 
        - 패키지 추가 설치
          ```bash
          # mac에서는 brew로 설치
          $ brew install postgis
          ```
        - postgis extension 설정
          ```sql
          CREATE EXTENSION postgis;
          ```
    1. SQLite
        - [GeoDjango - spatialite](https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/spatialite/#installing-spatialite)
        - 패키지 추가 설치
          ```bash
          # mac - homebrew
          $ brew install spatialite-tools
          ```
          > For example, on Debian-based distributions, try to install the *spatialite-bin* package. For distributions that package SpatiaLite 4.2+, install *libsqlite3-mod-spatialite*
          SPATIALITE_LIBRARY_PATH setting required for SpatiaLite 4.2+
          If you’re using SpatiaLite 4.2+, you must put this in your settings.py:  
          ```SPATIALITE_LIBRARY_PATH = 'mod_spatialite'```
        - settings.py 설정 
          ```python
          SPATIALITE_LIBRARY_PATH='/usr/local/lib/mod_spatialite.dylib'
          ```
3. settings.py - Database Engine
    - [GeoDjango - Spatial Backends](https://docs.djangoproject.com/en/2.0/ref/contrib/gis/db-api/#geodjango-database-api)
      + django.contrib.gis.db.backends.postgis
      + django.contrib.gis.db.backends.mysql
      + django.contrib.gis.db.backends.oracle
      + django.contrib.gis.db.backends.spatialite
    - INSTALLED_APPS `django.contrib.gis`추가

### AWS환경

- Python (3.6)
- S3 Bucket, 해당 Bucket을 사용할 수 있는 IAM User의 AWS AccessKey, SecretAccessKey
- RDS Database(보안 그룹 허용 필요), 해당 Database를 사용할 수 있는 RDS의 User, Password

## Installation (Django runserver)

### 로컬 환경

```
pip install -r .requirements/dev.txt
python manage.py runserver
```

### AWS 환경

```
export DJANGO_SETTINGS_MODULE=config.settings.dev
pip install -r .requirements/dev.txt
python manage.py runserver
```

### 배포 환경

```
export DJANGO_SETTINGS_MODULE=config.settings.production
pip install -r .requirements/dev.txt
python manage.py runserver
```

## Installation (Docker)

### 로컬 환경

`localhost:8000` 에서 확인

```
docker build -t overeats:local -f Dockerfile.local
docker run --rm -it 8000:80 overeats:local
```

### AWS 환경 (개발 모드)

```
docker build -t overeats:dev -f Dockerfile.dev
docker run --rm -it 8000:80 overeats:dev
```

### AWS 환경 (배포 모드)

```
docker build -t overeatsr:production -f Dockerfile.production
docker run --rm -it 8000:80 overeats:production
```

## DockerHub 관련

apt, pip관련 내용을 미리 빌드해서 DockerHub 저장소에 업로드

```
docker build -t eb-docker:base -f Dockerfile.base
docker tag eb-docker:base <자신의 사용자명>/<저장소명>:base
docker push <사용자명>/<저장소명>:base
```

이후 ElasticBeanstalk을 사용한 배포 시, 해당 이미지를 사용

```dockerfile
FROM    <사용자명/<저장소명>:base
...
...
```

## Deploy

`.deploy.sh`파일을 사용

```
./deploy.sh
```

## .secrets

### .secrets/base.json

```json
    {
      "SECRET_KEY": "<Django secret key>",
      "RAVEN_CONFIG": {
        "dsn": "https://<Sentry secret key>@sentry.io/300780",
        "release": "raven.fetch_git_sha(os.path.abspath(os.pardir))"
      },
      "SUPERUSER_USERNAME": "<Default superuser username>",
      "SUPERUSER_PASSWORD": "<Default superuser password>",
      "SUPERUSER_EMAIL": "<Default superuser email>",

      "AWS_ACCESS_KEY_ID": "<AWS access key (Permission: S3)>",
      "AWS_SECRET_ACCESS_KEY": "<AWS secret access key>",
      "AWS_STORAGE_BUCKET_NAME": "<AWS S3 Bucket name>",
      "AWS_S3_REGION_NAME": "<AWS Bucket region",
      "AWS_S3_SIGNATURE_VERSION": "s3v4",
      "AWS_DEFAULT_ACL": "private"
    }
```

### .secrest/dev.json, .secrets/production.json

```json
{
  "DATABASES": {
    "default": {
      "ENGINE": "django.db.backends.postgis",
      "HOST": "<AWS RDS end-point>",
      "NAME": "<DB name>",
      "USER": "<DB username>",
      "PASSWORD": "<DB user password",
      "PORT": 5432
    }
  }
}
```

good luck