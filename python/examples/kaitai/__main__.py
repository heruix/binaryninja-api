#!/usr/bin/env python

# test script

from __future__ import print_function

import io
import sys
import types
import importlib


if sys.version_info[0] == 2:
	import kaitaistruct
	import kshelpers
else:
	from . import kaitaistruct
	from . import kshelpers

NORMAL = '\033[0m'
BLACK = '\033[0;30m'
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
BLUE = '\033[0;34m'
PURPLE = '\033[0;35m'
CYAN = '\033[0;36m'
GRAY = '\033[0;37m'

LBLACK = '\033[1;30m'
LRED = '\033[1;31m'
LGREEN = '\033[1;32m'
LYELLOW = '\033[1;33m'
LBLUE = '\033[1;34m'
LPURPLE = '\033[1;35m'
LCYAN = '\033[1;36m'
LGRAY = '\033[1;37m'

def dump(obj, depth=0):
	dump_exceptions = ['_root', '_parent', '_io', 'SEQ_FIELDS']

	indent = '    '*depth

	if isinstance(obj, kaitaistruct.KaitaiStruct):
		fieldNames = []
		for candidate in dir(obj):
			if candidate != '_debug' and candidate.startswith('_'):
				continue
			if candidate in dump_exceptions:
				continue
			try:
				if getattr(obj, candidate, False):
					fieldNames.append(candidate)
			except Exception:
				pass

		for fieldName in fieldNames:
			subObj = getattr(obj, fieldName)

			if type(subObj) == types.MethodType:
				pass
			#elif type(subObj) == types.TypeType:
			elif isinstance(subObj, type):
				pass
			elif fieldName == '_debug':
				print(('%s._debug:'+RED+' %s'+NORMAL) % (indent, repr(subObj)))
			#elif type(subObj) == types.ListType:
			elif isinstance(subObj, list):
				if len(subObj)>0 and isinstance(subObj[0], kaitaistruct.KaitaiStruct):
					for i in range(len(subObj)):
						print('%s.%s[%d]:' % (indent, fieldName, i))
						dump(subObj[i], depth+1)
				else:
					print('%s.%s: %s' % (indent, fieldName, str(subObj)))
			#elif type(subObj) == types.DictionaryType:
			elif isinstance(subObj, dict):
				print('%s.%s: %s' % (indent, fieldName, subObj))

			#elif type(subObj) == types.StringType:
			elif isinstance(subObj, str):
				if len(subObj) <= 16:
					print(('%s.%s: '+CYAN+'%s'+NORMAL) % (indent, fieldName, repr(subObj)))
				else:
					print(('%s.%s: '+CYAN+'%s...'+NORMAL+' 0x%X (%d) bytes total') % \
						(indent, fieldName, repr(subObj[0:16]), len(subObj), len(subObj))
					)

			elif type(subObj) == int:
				print(('%s.%s: '+YELLOW+'0x%X '+NORMAL+'('+YELLOW+'%d'+NORMAL+')') % (indent, fieldName, subObj, subObj))

			elif str(type(subObj)).startswith('<enum '):
				print(('%s.%s: '+'%s') % (indent, fieldName, repr(subObj)))

			elif isinstance(subObj, kaitaistruct.KaitaiStruct):
				print('%s.%s:' % (indent, fieldName))
				dump(subObj, depth+1)

			else:
				print('%s.%s: %s' % (indent, fieldName, type(subObj)))
	else:
		print((PURPLE+'%s%s'+NORMAL) % (indent, repr(obj)))
		#else:
		#	print('%s%s: %s' % (indent, fieldName, repr(subObj)))

if __name__ == '__main__':
	if not sys.argv[1:]:
		raise Exception('expected arguments')

	cmd = sys.argv[1]

	if cmd == 'dump':
		fpath = sys.argv[2]
		parsed = kshelpers.parseFpath(fpath)
		dump(parsed)

	if cmd == 'import':
		print('importing every format...')

		module_names = [
		'aix_utmp', 'allegro_dat', 'andes_firmware', 'apm_partition_table',
		'apple_single_double', 'asn1_der', 'avantes_roh60', 'avi', 'bcd',
		'bitcoin_transaction', 'blender_blend', 'bmp', 'bson', 'code_6502', 'cpio_old_le',
		'cramfs', 'creative_voice_file', 'dbf', 'dex', 'dicom', 'dns_packet', 'doom_wad',
		'dos_mz', 'dune_2_pak', 'edid', 'elf', 'exif', 'exif_be', 'exif_le',
		'ext2', 'fallout2_dat', 'fallout_dat', 'fasttracker_xm_module', 'ftl_dat',
		'genmidi_op2', 'gettext_mo', 'gif', 'glibc_utmp', 'google_protobuf',
		'gpt_partition_table', 'gran_turismo_vol', 'gzip', 'hccap', 'hccapx', 'heaps_pak',
		'heroes_of_might_and_magic_agg', 'heroes_of_might_and_magic_bmp', 'icc_4',
		'icmp_packet', 'ico', 'id3v1_1', 'id3v2_3', 'id3v2_4', 'ines',
		'iso9660', 'java_class', 'jpeg', 'luks', 'lvm2', 'lzh', 'mach_o',
		'magicavoxel_vox', 'mbr_partition_table', 'microsoft_cfb',
		'microsoft_pe', 'mifare_classic',
		'monomakh_sapr_chg', 'msgpack', 'nt_mdt', 'nt_mdt_pal', 'ogg', 'openpgp_message',
		'pcx', 'pcx_dcx', 'png', 'psx_tim',
		'python_pyc_27', 'quake_mdl', 'quake_pak', 'quicktime_mov', 'rar', 'regf',
		'renderware_binary_stream', 'rtcp_payload', 'rtp_packet', 'ruby_marshal', 's3m',
		'saints_row_2_vpp_pc', 'shapefile_index', 'shapefile_main', 'specpr', 'sqlite3',
		'ssh_public_key', 'standard_midi_file', 'stl', 'swf', 'systemd_journal',
		'tcp_segment', 'tga', 'tls_client_hello', 'tr_dos_image', 'tsm', 'ttf',
		'udp_datagram', 'uimage', 'vdi', 'vfat', 'vlq_base128_be', 'vlq_base128_le',
		'vmware_vmdk', 'vp8_ivf', 'warcraft_2_pud', 'wav', 'windows_evt_log',
		'windows_lnk_file', 'windows_minidump', 'windows_resource_file',
		'windows_shell_items', 'windows_systemtime', 'wmf', 'xwd', 'zip',
		]

		if sys.version_info[0] == 3:
			module_names += ['ipv4_packet', 'ipv6_packet', 'protocol_body',
				'microsoft_network_monitor_v2', 'packet_ppi', 'pcap',
				'ethernet_frame']

		(npass, nfail) = (0,0)

		for module_name in sorted(module_names):
			class_name = ''.join(map(lambda x: x.capitalize(), module_name.split('_')))

			print('from %s import %s...' % (module_name, class_name), end='')
			try:
				module = importlib.import_module('.'+module_name, 'kaitai')
				method = getattr(module, class_name)
				print('['+GREEN+'PASS'+NORMAL+']')
				npass += 1
			except Exception as e:
				print('['+RED+str(e)+NORMAL+']')
				nfail += 1

		ntests = 1.0*npass + nfail
		assert(ntests == len(module_names))
		print('passes %d of %d (rate: %0.1f%%)' % (npass, ntests, 100*npass/ntests))
		print('failures %d of %d (rate: %0.1f%%)' % (nfail, ntests, 100*nfail/ntests))

	if cmd == 'dumpbinja':
		fpath = sys.argv[2]
		import binaryninja
		binaryView = binaryninja.BinaryViewType['Raw'].open(fpath)
		kaitaiIo = KaitaiBinaryViewIO(binaryView)
		parsed = parse_io(kaitaiIo)
		print(parsed.header.program_headers)

