from setuptools import setup, find_packages

setup(
    name="iotile_support_exec_nrf52832_3",
    packages=find_packages(include=["iotile_support_exec_nrf52832_3.*", "iotile_support_exec_nrf52832_3"]),
    version="3.1.3",
    install_requires=['iotile_support_lib_controller_4 >= 4.3.5, == 4.*'],
    entry_points={'iotile.proxy': ['nrf52832_safemode = iotile_support_exec_nrf52832_3.nrf52832_safemode']},
    include_package_data=True,
    author="Arch",
    author_email="info@arch-iot.com"
)