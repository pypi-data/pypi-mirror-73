from setuptools import setup

setup(
    name='Claver-Message-Board',
    version='0.0.2',
    packages=['interface', 'interface.gui', 'interface.news', 'interface.games', 'interface.lists', 'interface.timer',
              'interface.doodle', 'interface.photos', 'interface.widgets', 'interface.calendar', 'interface.messages',
              'interface.settings', 'interface.settings.categories'],
    url='https://github.com/mccolm-robotics/Claver-Interactive-Message-Board',
    license='MIT',
    author='Praxis',
    author_email='simulacra.mechatronics@gmail.com',
    description='Interactive messaging board for RPi'
)
