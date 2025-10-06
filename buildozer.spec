[app]
# 앱 제목, 패키지 이름, 버전
title = Quiz
package.name = quiz
package.domain = org.test
version = 1.0

# 소스 디렉토리 및 포함할 파일 확장자
source.dir = .
source.include_exts = py,png,jpg,ttf,csv

# 앱 아이콘 경로
icon.filename = %(source.dir)s/quizicon.png

# 필요 라이브러리 (pillow 추가)
requirements = python3,kivy==2.2.1,pillow

# 화면 방향
orientation = portrait

[android]
# 라이선스 자동 동의
android.accept_sdk_license = True

# 안드로이드 API 레벨 및 NDK 버전
android.api = 33
android.minapi = 21
android.sdk = 24
android.ndk = 25b

# 지원 CPU 아키텍처
android.archs = arm64-v8a, armeabi-v7a

# 필요 권한
android.permissions = INTERNET,VIBRATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# python-for-android 브랜치
p4a.branch = master
