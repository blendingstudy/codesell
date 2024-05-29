import os
import subprocess
import uuid

def create_code_directory(code_file_path):
    unique_directory = str(uuid.uuid4())
    code_directory = os.path.join(os.path.dirname(code_file_path), 'sandbox', unique_directory)
    os.makedirs(code_directory, exist_ok=True)
    return code_directory

def copy_code_file(code_file_path, code_directory):
    code_filename = os.path.basename(code_file_path)
    sandbox_code_path = os.path.join(code_directory, code_filename)
    os.replace(code_file_path, sandbox_code_path)
    return sandbox_code_path

def create_dockerfile(code_directory, code_filename):
    dockerfile_path = os.path.join(code_directory, 'Dockerfile')
    with open(dockerfile_path, 'w') as f:
        f.write('FROM python:3.9\n')
        f.write('WORKDIR /app\n')
        f.write(f'COPY {code_filename} /app/\n')
        f.write('COPY requirements.txt /app/\n')
        f.write('RUN pip install -r requirements.txt\n')
        f.write('CMD ["python", "app.py"]\n')

def create_requirements_file(code_directory):
    requirements_path = os.path.join(code_directory, 'requirements.txt')
    with open(requirements_path, 'w') as f:
        f.write('Flask==2.0.1\n')
        f.write('werkzeug==2.0.1\n')
        f.write('# Add other required packages\n')

def build_and_deploy_code(code_file_path):
    code_directory = create_code_directory(code_file_path)
    code_filename = os.path.basename(code_file_path)
    sandbox_code_path = copy_code_file(code_file_path, code_directory)
    create_dockerfile(code_directory, code_filename)
    create_requirements_file(code_directory)

    # 코드 빌드 명령어 실행
    build_command = f"docker build -t code-sandbox-{os.path.basename(code_directory)} -f {os.path.join(code_directory, 'Dockerfile')} {code_directory}"
    subprocess.run(build_command, shell=True, check=True)

    print("코드 빌드 완료")

    # 빌드된 이미지 ID 가져오기
    image_id = subprocess.check_output(f"docker images -q code-sandbox-{os.path.basename(code_directory)}", shell=True).strip().decode()

    return image_id