# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function
import os
import sys
import shutil

import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)

try:
    import SCons.Script as SCons
except:
    import scons
    for path in scons.__path__:
        sys.path.append(path)
        import SCons.Script as SCons

from .log import logger
from .toolchain import *


class Builder(object):
    def __init__(self, solution):
        self.toolchain_path = ''
        self.PREFIX = 'csky-abiv2-elf'
        if solution.toolchain_prefix:
            self.PREFIX = solution.toolchain_prefix
        self.SIZE = lambda: self.PREFIX + '-size'
        self.OBJDUMP = lambda: self.PREFIX + '-objdump'
        self.OBJCOPY = lambda: self.PREFIX + '-objcopy'
        self.STRIP = lambda: self.PREFIX + '-strip'
        self.AS = lambda: self.PREFIX + '-gcc'
        self.CC = lambda: self.PREFIX + '-gcc'
        self.CXX = lambda: self.PREFIX + '-g++'
        self.AR = lambda: self.PREFIX + '-ar'
        self.LINK = lambda: self.PREFIX + '-g++'

        self.solution = solution

        self.env = SCons.Environment(tools=['default', 'objcopy', 'objdump', 'product'],
                                     toolpath=[os.path.dirname(
                                         __file__) + '/site_tools'],
                                     AS=self.AS(),
                                     CC=self.CC(),
                                     CXX=self.CXX(),
                                     AR=self.AR(),
                                     LINK=self.CXX(),
                                     OBJCOPY=self.OBJCOPY(),
                                     OBJDUMP=self.OBJDUMP(),
                                     ARFLAGS='-rc',
                                     )

        # self.env.Decider(decide_if_changed)
        self.env.Decider('timestamp-newer')
        # self.env.Decider('make')
        # self.env.Decider('MD5')

        self.env.PrependENVPath('TERM', "xterm-256color")
        self.env.PrependENVPath('PATH', os.getenv('PATH'))

        if SCons.GetOption('verbose'):
            self.env.Replace(
                ARCOMSTR='AR $TARGET',
                ASCOMSTR='AS $TARGET',
                ASPPCOMSTR='AS $TARGET',
                CCCOMSTR='CC $TARGET',
                CXXCOMSTR='CXX $TARGET',
                LINKCOMSTR = 'LINK $TARGET',
                INSTALLSTR='INSTALL $TARGET',
                BINCOMSTR="Generating $TARGET",
            )

        self.set_cpu(self.solution.cpu_name)
        if self.solution.LINKFLAGS:
            linkflags = self.solution.LINKFLAGS
        else:
            if self.solution.cpu_name.lower().startswith('ck'):
                linkflags = ['-lm', '-Wl,-ckmap="yoc.map"', '-Wl,-zmax-page-size=1024']
            else:
                linkflags = ['-lm', '-Wl,-Map="yoc.map"', '-Wl,-zmax-page-size=1024']
        self.env.AppendUnique(
            ASFLAGS=self.solution.ASFLAGS,
            CCFLAGS=self.solution.CCFLAGS,
            CXXFLAGS=self.solution.CXXFLAGS,
            LINKFLAGS=linkflags,
        )

        self.env.Replace(AS=self.AS(),
                        CC=self.CC(),
                        CXX=self.CXX(),
                        AR=self.AR(),
                        LINK=self.CXX(),
                        OBJCOPY=self.OBJCOPY(),
                        OBJDUMP=self.OBJDUMP())

    def set_cpu(self, cpu):
        flags = ['-MP', '-MMD', '-g', '-Os', '-Wno-main']
        self.CPU = cpu.lower()
        if self.CPU in ['ck801', 'ck802', 'ck803', 'ck804', 'ck805', 'ck803f', 'ck803ef', 'ck803efr1', 'ck804ef', 'ck805f', 'ck805ef']:
            if not self.PREFIX:
                self.PREFIX = 'csky-abiv2-elf'
            flags.append('-mcpu=' + self.CPU)
            if 'f' in self.CPU:
                flags.append('-mhard-float')
            if self.CPU == 'ck803ef':
                flags.append('-mhigh-registers')
                flags.append('-mdsp')
        elif self.CPU in ['rv32emc', 'e902', 'e906', 'e906f', 'e906fd']:
            if not self.PREFIX:
                self.PREFIX = 'riscv64-unknown-elf'
            if self.CPU == 'rv32emc':
                flags.append('-march=' + self.CPU)
                flags.append('-mabi=ilp32e')
            if self.CPU == 'e902':
                flags.append('-march=rv32ecxthead')
                flags.append('-mabi=ilp32e')
            if self.CPU == 'e906':
                flags.append('-march=rv32imacxthead')
                flags.append('-mabi=ilp32')
                flags.append('-mcmodel=medlow')
            if self.CPU == 'e906f':
                flags.append('-march=rv32imafcxthead')
                flags.append('-mabi=ilp32f')
                flags.append('-mcmodel=medlow')
            if self.CPU == 'e906fd':
                flags.append('-march=rv32imafdcxthead')
                flags.append('-mabi=ilp32d')
                flags.append('-mcmodel=medlow')
        elif self.CPU in ['arm1020e', 'arm1020t', 'arm1022e', 'arm1026ej-s', 'arm10e', 'arm10tdmi', 'arm1136j-s', 'arm1136jf-s', 'arm1156t2-s',
                            'arm1156t2f-s', 'arm1176jz-s', 'arm1176jzf-s', 'arm2', 'arm250', 'arm3', 'arm6', 'arm60', 'arm600', 'arm610', 'arm620',
                            'arm7', 'arm70', 'arm700', 'arm700i', 'arm710', 'arm7100', 'arm710c', 'arm710t', 'arm720', 'arm720t', 'arm740t', 'arm7500',
                            'arm7500fe', 'arm7d', 'arm7di', 'arm7dm', 'arm7dmi', 'arm7m', 'arm7tdmi', 'arm7tdmi-s', 'arm8', 'arm810', 'arm9', 'arm920',
                            'arm920t', 'arm922t', 'arm926ej-s', 'arm940t', 'arm946e-s', 'arm966e-s', 'arm968e-s', 'arm9e', 'arm9tdmi', 'cortex-a12',
                            'cortex-a15', 'cortex-a17', 'cortex-a32', 'cortex-a35', 'cortex-a5','cortex-a53', 'cortex-a57', 'cortex-a7', 'cortex-a72',
                            'cortex-a73', 'cortex-a8', 'cortex-a9', 'cortex-m0', 'cortex-m0.small-multiply', 'cortex-m0plus', 'cortex-m0plus.small-multiply',
                            'cortex-m1', 'cortex-m1.small-multiply', 'cortex-m23', 'cortex-m3', 'cortex-m33', 'cortex-m33+nodsp', 'cortex-m4', 'cortex-m7',
                            'cortex-r4', 'cortex-r4f', 'cortex-r5', 'cortex-r52', 'cortex-r7', 'cortex-r8']:
            if not self.PREFIX:
                self.PREFIX = 'arm-none-eabi'
            flags.append('-mcpu=' + self.CPU)
        else:
            logger.error(
                'error cpu `%s`, please make sure your cpu mode' % self.CPU)
            exit(0)

        self.env.AppendUnique(
            ASFLAGS=flags, CCFLAGS=flags,
            CXXFLAGS=flags, LINKFLAGS=flags
        )

    def clone_component(self, component):
        def var_convert(defs):
            if type(defs) == dict:
                vars = {}
                for k, v in defs.items():
                    if type(v) == str:
                        vars[k] = '\\"' + v + '\\"'
                    else:
                        vars[k] = v
                return vars
            else:
                return defs

        env = self.env.Clone()

        if component.build_config.cflag:
            env.AppendUnique(CCFLAGS=component.build_config.cflag.split())
            env.AppendUnique(CCFLAGS=component.build_config.cflag.split())
        if component.build_config.cxxflag:
            env.AppendUnique(CPPFLAGS=component.build_config.cxxflag.split())
        if component.build_config.asmflag:
            env.AppendUnique(ASFLAGS=component.build_config.asmflag.split())

        env.AppendUnique(CPPPATH=component.build_config.internal_include)
        env.AppendUnique(CPPPATH=self.solution.global_includes)
        env.AppendUnique(CPPDEFINES=var_convert(self.solution.defines))
        env.AppendUnique(CPPDEFINES=var_convert(component.build_config.define))

        if self.toolchain_path == '':
            tool = ToolchainYoC()
            path = tool.check_toolchain(self.PREFIX)
            if path:
                self.toolchain_path = os.path.dirname(path)
        if self.toolchain_path:
            env.PrependENVPath('PATH', self.toolchain_path)
        else:
            put_string("Not found toolchain: `%s`, please check it." % self.PREFIX)
            exit(-1)

        return env

    def build_component(self, component):
        env = self.clone_component(component)

        sources = []
        for fn in component.source_files:
            f_list = env.Glob(fn)
            if f_list:
                for f in f_list:
                    if f not in sources:
                        sources.append(f)

        job = env.StaticLibrary(os.path.join(
            self.solution.lib_path, component.name), sources)

        env.Default(job)

        if component.type == 'solution':
            linkflags = ' -Wl,--whole-archive -l' + \
                ' -l'.join(self.solution.libs) + ' -l' + component.name + ' -Wl,--no-whole-archive'
            linkflags += ' -nostartfiles -Wl,--gc-sections'
            linkflags += ' -T ' + self.solution.ld_script
            cname = 'yoc'  # component.name
            env.AppendUnique(LINKFLAGS=linkflags.split())
            env.AppendUnique(LIBPATH=self.solution.libpath)
            job = env.Program(target=cname + '.elf', source=[])

            # add recompiled file check.
            env.Depends(job, self.solution.depend_libs)
            env.Depends(job, self.solution.ld_script)
            env.Default(job)

            jobs = []
            dirname = os.path.dirname(env.GetBuildPath("output_xxxd"))
            if env['ELF_FILE']:
                output = os.path.join(dirname, env['ELF_FILE'])
                jj = env.InstallAs(output, job[0])
                jobs.append(jj)

            if env['OBJCOPY_FILE']:
                output = os.path.join(dirname, env['OBJCOPY_FILE'])
                jj = env.Binary(source=job[0], target=output)
                jobs.append(jj)

            if env['OBJDUMP_FILE']:
                output = os.path.join(dirname, env['OBJDUMP_FILE'])
                jj = env.Dump(source=job[0], target=output)
                jobs.append(jj)

            env.Default(jobs)

    def build_image(self, elf=None, objcopy=None, objdump=None, product=None):
        component = self.solution.solution_component
        env = self.clone_component(component)

        source_name = os.path.join('out', component.name, 'yoc.elf')
        if elf and os.path.isfile(source_name):
            shutil.copy2(source_name, elf)


        if objcopy:
            job1 = env.Binary(source=source_name, target=objcopy)
            env.Default(job1)

        if objdump:
            job2 = env.Dump(source=source_name, target=objdump)
            env.Default(job2)
        if product:
            job3 = env.Zip(source='generated/data/config.yaml',
                        target="generated/images.zip", PATH='generated/data')
            job4 = env.Hex(source='generated/images.zip', PATH='generated')
            env.Default(job3)
            env.Default(job4)


def decide_if_changed(dependency, target, prev_ni, repo_node=None):
    # put_string(dependency, prev_ni)
    if not prev_ni:
        return True
    if dependency.get_timestamp() != prev_ni.timestamp:
        return True

    return False
