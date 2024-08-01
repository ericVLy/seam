# node_dependency_checker/management/commands/install_node_dependencies.py
import os
import logging
import subprocess
from django.conf import settings
from django.core.management.base import BaseCommand


currentPath = os.path.split(os.path.realpath(__file__))[0]
projectRootPath = os.path.abspath(os.path.join(currentPath, '..', '..', '..'))

static_path = os.path.join(projectRootPath, 'personal_matters', 'static')
vendor_static_path = os.path.join(static_path, "vendor")


log = logging.getLogger('django')


class Command(BaseCommand):
    help = 'Check and install Node.js dependencies'

    def handle(self, *args, **options):
        try:
            # 检查 Node.js 是否可用
            subprocess.run('node --version', shell=True, check=True)
            subprocess.run('npm --version', shell=True, check=True)
            log.info('Node.js is installed.')

            # 检查并安装 Node.js 依赖
            npm_mirror = os.environ.get("npm_mirror", None)
            if npm_mirror is not None:
                log.info(f"npm_mirror: {npm_mirror}")
                subprocess.run(f'npm config set registry {npm_mirror}', shell=True)
            log.info(static_path)
            subprocess.run('npm install', shell=True, check=True, cwd=static_path)
            log.info('Node.js dependencies installed successfully.')
            with open(os.path.join(static_path, "package.json"), "r", encoding="utf-8") as package_file:
                import json
                import shutil
                packages = json.load(package_file)["dependencies"]  # type: dict
                if not os.path.exists(vendor_static_path):
                    os.makedirs(vendor_static_path)
                else:
                    shutil.rmtree(vendor_static_path)
                for package_name, pgk_ver in packages.items():
                    package_path = os.path.join(static_path, "node_modules", str(package_name))
                    if str(package_name).startswith("@"):
                        package_name = str(package_name).split("@")[1]  # type: str
                    if os.path.exists(package_path):
                        log.info(f"move {package_name} from {package_path}")
                        shutil.move(package_path, os.path.join(vendor_static_path, str(package_name)))
                    else:
                        log.error(f"path: '{package_path}' not exists")
                shutil.rmtree(os.path.join(static_path, "node_modules"))


        except FileNotFoundError:
            log.error('Node.js is not installed. Please install Node.js and npm first.')
            raise FileNotFoundError('Node.js is not installed. Please install Node.js and npm first.')

        except subprocess.CalledProcessError as e:
            log.error('An error occurred while installing Node.js dependencies:', e)
            raise e
