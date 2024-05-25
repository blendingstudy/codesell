import os
import subprocess

def build_and_deploy_code(code_directory):
    # 코드 빌드 명령어 실행
    build_command = f"cd {code_directory} && make build"
    subprocess.run(build_command, shell=True, check=True)

    # Docker 이미지 빌드 명령어 실행
    docker_build_command = f"cd {code_directory} && docker build -t code-sandbox ."
    subprocess.run(docker_build_command, shell=True, check=True)

    # Docker 컨테이너 실행 명령어 실행
    docker_run_command = "docker run -d --name code-sandbox-container code-sandbox"
    subprocess.run(docker_run_command, shell=True, check=True)

    print("코드 빌드 및 샌드박스 환경 배포 완료")

# 업로드된 코드의 저장 경로
uploaded_code_directory = "/path/to/uploaded/code/"

# 자동화 스크립트 실행
build_and_deploy_code(uploaded_code_directory)