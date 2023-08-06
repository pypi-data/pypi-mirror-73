from setuptools import setup, find_packages

setup(
    name = 'pythonpook',
    version = '1.0.0',
    packages = find_packages(),

    # 作者、プロジェクト情報
    autor = 'katuhito hara',
    author_email = 'katuhitohara@gmail.com',

    # プロジェクトホームページのURL

    url = 'https://github.com/katuhito/pythonpook',

    # 短い説明文と長い説明文を用意
    # content_typeは下記のいずれか
    # text/plain, text/x-rst,text/markdown

    descripsion = 'This is a test package for me.',

    long_description = open('README.md').read(),

    long_description_content_type = 'text/markdown',

        # Pythonバージョンは3.6以上で4未満
    python_requires = '~=3.6',

        # PyPI上での検索、閲覧のために利用される
        # ライセンス、Pythonバージョン、OSを含めること

    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',

        ],

    install_requires = [
        # Clickのバージョンは7.0以上8未満
        'Click~=7.0',

        # sampleprojectをコミットを指定して取得

        # 'sampleproject@git+https://github.com/pypa/sampleproject#sha1=2cf198529c6c5a4fa50c28505ce6a90266b89868',
        ],

    extras_require = {
            's3': ['boto3~=1.10.0'],
            'gcs': ['google-cloud-storage~=1.23.0'],
        },

    package_data = {'pythonpook': ['data/*']},

)
