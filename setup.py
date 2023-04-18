from setuptools import setup
import pygccx

setup(
    
    name=pygccx.__name__,
    version=pygccx.__version__,
    author=pygccx.__author__,
    author_email=pygccx.__author_email__,
    python_requires='>=3.10, <4',
    packages=['pygccx',
                'pygccx.test', 
                'pygccx.helper_features', 'pygccx.helper_features.test',
                'pygccx.mesh', 'pygccx.mesh.test', 'pygccx.mesh.mesh_factory',
                'pygccx.model_keywords', 'pygccx.model_keywords.test',
                'pygccx.result_reader', 'pygccx.result_reader.test',
                'pygccx.step_keywords', 'pygccx.step_keywords.test',
                'pygccx.tools', 'pygccx.tools.stress_tools', 
                'pygccx.tools.stress_tools.test',
                'pygccx.tools.stress_tools.test.test_data'],
    include_package_data=True,
    license='LICENSE',
    description='A python framework for CalculiX',
    install_requires=['numpy >= 1.22.4',
                      'scipy >= 1.9.0',
                      'gmsh >= 4.10.3']
    )