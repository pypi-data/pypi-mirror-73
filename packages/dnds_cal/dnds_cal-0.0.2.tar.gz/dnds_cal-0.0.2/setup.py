import setuptools

setuptools.setup(
    name="dnds_cal",
    version="0.0.2",
    author="Zhu Tao",
    author_email="zhutao@cau.edu.cn",
    description="Calculate the dn/ds (also pn and ps) value of cds",
    url="https://github.com/zhutao1009/dnds",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
python_requires='>=3.0'
)