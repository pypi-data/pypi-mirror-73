from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='pyleafarea',
    version='2.2',
    packages=['pyleaf'],
    url='',
    license='MIT License',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'Keras>=2.2.4',
        'numpy>=1.15.2',
        'pandas>=0.23.0',
        'Pillow>=5.3.0',
        'tensorflow==1.12.0',
        'tensorboard==1.12.0',
        'Keras-Applications>=1.0.6',
        'Keras-Preprocessing>=1.0.5',
        'protobuf>=3.6.1',
        'pyzbar>=0.1.8',
        'opencv-python>=3.4.3.18'
        ],
    tests_require=["pytest"],
    include_package_data=True,
    author='Vishal Sonawane, Balasaheb Sonawane',
    author_email='vishalsonawane1515@gmail.com, balasahebsonawane@gmail.com',
    description='Automated Leaf Area Calculator Using Tkinter and Deep Learning Image Classification Model.'
)