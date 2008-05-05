from distutils.core import setup

setup(name='djangoamf',
    version='0.6',
    author='otsuka',
    author_email='otsuka@users.sourceforge.jp',
    description="Django AMF is a Middleware for Django web framework written in Python. It enables Flash/Flex applications to invoke Django's view functions with AMF(Action Message Format).",
    url='http://djangoamf.sourceforge.jp/',
    packages=['amf', 'amf.django', 'amf.django.middleware'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'License :: OSI Approved :: GPL License',
        'Intentded Audience :: Developers',
        ],
    )

