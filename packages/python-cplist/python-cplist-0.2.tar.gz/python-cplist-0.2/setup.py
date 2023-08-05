import setuptools

cplist = setuptools.Extension('cplist', sources=['plist.c'], libraries=['plist'], extra_compile_args=['-std=c99'], extra_objects=['/usr/local/lib/libplist.a'])

setuptools.setup(
        name='python-cplist',
        author="Jonathan Goren",
        author_email="jonagn@gmail.com",
        description="CPython property list parser",
        version="0.2",
        ext_modules = [cplist],
        )
