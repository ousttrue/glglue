'''
https://github.khronos.org/KTX-Specification/
# _anchor_id_basicdescriptor_xreflabel_basicdescriptor_khronos_basic_data_format_descriptor_block
* https://www.khronos.org/registry/DataFormat/specs/1.3/dataformat.1.3.html
'''
import pathlib
import struct
from typing import NamedTuple, List, Dict, Any
from enum import Enum


class VkFormat(Enum):
    '''
    https://www.khronos.org/registry/vulkan/specs/1.2-extensions/man/html/VkFormat.html
    '''
    VK_FORMAT_UNDEFINED = 0
    VK_FORMAT_R4G4_UNORM_PACK8 = 1
    VK_FORMAT_R4G4B4A4_UNORM_PACK16 = 2
    VK_FORMAT_B4G4R4A4_UNORM_PACK16 = 3
    VK_FORMAT_R5G6B5_UNORM_PACK16 = 4
    VK_FORMAT_B5G6R5_UNORM_PACK16 = 5
    VK_FORMAT_R5G5B5A1_UNORM_PACK16 = 6
    VK_FORMAT_B5G5R5A1_UNORM_PACK16 = 7
    VK_FORMAT_A1R5G5B5_UNORM_PACK16 = 8
    VK_FORMAT_R8_UNORM = 9
    VK_FORMAT_R8_SNORM = 10
    VK_FORMAT_R8_USCALED = 11
    VK_FORMAT_R8_SSCALED = 12
    VK_FORMAT_R8_UINT = 13
    VK_FORMAT_R8_SINT = 14
    VK_FORMAT_R8_SRGB = 15
    VK_FORMAT_R8G8_UNORM = 16
    VK_FORMAT_R8G8_SNORM = 17
    VK_FORMAT_R8G8_USCALED = 18
    VK_FORMAT_R8G8_SSCALED = 19
    VK_FORMAT_R8G8_UINT = 20
    VK_FORMAT_R8G8_SINT = 21
    VK_FORMAT_R8G8_SRGB = 22
    VK_FORMAT_R8G8B8_UNORM = 23
    VK_FORMAT_R8G8B8_SNORM = 24
    VK_FORMAT_R8G8B8_USCALED = 25
    VK_FORMAT_R8G8B8_SSCALED = 26
    VK_FORMAT_R8G8B8_UINT = 27
    VK_FORMAT_R8G8B8_SINT = 28
    VK_FORMAT_R8G8B8_SRGB = 29
    VK_FORMAT_B8G8R8_UNORM = 30
    VK_FORMAT_B8G8R8_SNORM = 31
    VK_FORMAT_B8G8R8_USCALED = 32
    VK_FORMAT_B8G8R8_SSCALED = 33
    VK_FORMAT_B8G8R8_UINT = 34
    VK_FORMAT_B8G8R8_SINT = 35
    VK_FORMAT_B8G8R8_SRGB = 36
    VK_FORMAT_R8G8B8A8_UNORM = 37
    VK_FORMAT_R8G8B8A8_SNORM = 38
    VK_FORMAT_R8G8B8A8_USCALED = 39
    VK_FORMAT_R8G8B8A8_SSCALED = 40
    VK_FORMAT_R8G8B8A8_UINT = 41
    VK_FORMAT_R8G8B8A8_SINT = 42
    VK_FORMAT_R8G8B8A8_SRGB = 43
    VK_FORMAT_B8G8R8A8_UNORM = 44
    VK_FORMAT_B8G8R8A8_SNORM = 45
    VK_FORMAT_B8G8R8A8_USCALED = 46
    VK_FORMAT_B8G8R8A8_SSCALED = 47
    VK_FORMAT_B8G8R8A8_UINT = 48
    VK_FORMAT_B8G8R8A8_SINT = 49
    VK_FORMAT_B8G8R8A8_SRGB = 50
    VK_FORMAT_A8B8G8R8_UNORM_PACK32 = 51
    VK_FORMAT_A8B8G8R8_SNORM_PACK32 = 52
    VK_FORMAT_A8B8G8R8_USCALED_PACK32 = 53
    VK_FORMAT_A8B8G8R8_SSCALED_PACK32 = 54
    VK_FORMAT_A8B8G8R8_UINT_PACK32 = 55
    VK_FORMAT_A8B8G8R8_SINT_PACK32 = 56
    VK_FORMAT_A8B8G8R8_SRGB_PACK32 = 57
    VK_FORMAT_A2R10G10B10_UNORM_PACK32 = 58
    VK_FORMAT_A2R10G10B10_SNORM_PACK32 = 59
    VK_FORMAT_A2R10G10B10_USCALED_PACK32 = 60
    VK_FORMAT_A2R10G10B10_SSCALED_PACK32 = 61
    VK_FORMAT_A2R10G10B10_UINT_PACK32 = 62
    VK_FORMAT_A2R10G10B10_SINT_PACK32 = 63
    VK_FORMAT_A2B10G10R10_UNORM_PACK32 = 64
    VK_FORMAT_A2B10G10R10_SNORM_PACK32 = 65
    VK_FORMAT_A2B10G10R10_USCALED_PACK32 = 66
    VK_FORMAT_A2B10G10R10_SSCALED_PACK32 = 67
    VK_FORMAT_A2B10G10R10_UINT_PACK32 = 68
    VK_FORMAT_A2B10G10R10_SINT_PACK32 = 69
    VK_FORMAT_R16_UNORM = 70
    VK_FORMAT_R16_SNORM = 71
    VK_FORMAT_R16_USCALED = 72
    VK_FORMAT_R16_SSCALED = 73
    VK_FORMAT_R16_UINT = 74
    VK_FORMAT_R16_SINT = 75
    VK_FORMAT_R16_SFLOAT = 76
    VK_FORMAT_R16G16_UNORM = 77
    VK_FORMAT_R16G16_SNORM = 78
    VK_FORMAT_R16G16_USCALED = 79
    VK_FORMAT_R16G16_SSCALED = 80
    VK_FORMAT_R16G16_UINT = 81
    VK_FORMAT_R16G16_SINT = 82
    VK_FORMAT_R16G16_SFLOAT = 83
    VK_FORMAT_R16G16B16_UNORM = 84
    VK_FORMAT_R16G16B16_SNORM = 85
    VK_FORMAT_R16G16B16_USCALED = 86
    VK_FORMAT_R16G16B16_SSCALED = 87
    VK_FORMAT_R16G16B16_UINT = 88
    VK_FORMAT_R16G16B16_SINT = 89
    VK_FORMAT_R16G16B16_SFLOAT = 90
    VK_FORMAT_R16G16B16A16_UNORM = 91
    VK_FORMAT_R16G16B16A16_SNORM = 92
    VK_FORMAT_R16G16B16A16_USCALED = 93
    VK_FORMAT_R16G16B16A16_SSCALED = 94
    VK_FORMAT_R16G16B16A16_UINT = 95
    VK_FORMAT_R16G16B16A16_SINT = 96
    VK_FORMAT_R16G16B16A16_SFLOAT = 97
    VK_FORMAT_R32_UINT = 98
    VK_FORMAT_R32_SINT = 99
    VK_FORMAT_R32_SFLOAT = 100
    VK_FORMAT_R32G32_UINT = 101
    VK_FORMAT_R32G32_SINT = 102
    VK_FORMAT_R32G32_SFLOAT = 103
    VK_FORMAT_R32G32B32_UINT = 104
    VK_FORMAT_R32G32B32_SINT = 105
    VK_FORMAT_R32G32B32_SFLOAT = 106
    VK_FORMAT_R32G32B32A32_UINT = 107
    VK_FORMAT_R32G32B32A32_SINT = 108
    VK_FORMAT_R32G32B32A32_SFLOAT = 109
    VK_FORMAT_R64_UINT = 110
    VK_FORMAT_R64_SINT = 111
    VK_FORMAT_R64_SFLOAT = 112
    VK_FORMAT_R64G64_UINT = 113
    VK_FORMAT_R64G64_SINT = 114
    VK_FORMAT_R64G64_SFLOAT = 115
    VK_FORMAT_R64G64B64_UINT = 116
    VK_FORMAT_R64G64B64_SINT = 117
    VK_FORMAT_R64G64B64_SFLOAT = 118
    VK_FORMAT_R64G64B64A64_UINT = 119
    VK_FORMAT_R64G64B64A64_SINT = 120
    VK_FORMAT_R64G64B64A64_SFLOAT = 121
    VK_FORMAT_B10G11R11_UFLOAT_PACK32 = 122
    VK_FORMAT_E5B9G9R9_UFLOAT_PACK32 = 123
    VK_FORMAT_D16_UNORM = 124
    VK_FORMAT_X8_D24_UNORM_PACK32 = 125
    VK_FORMAT_D32_SFLOAT = 126
    VK_FORMAT_S8_UINT = 127
    VK_FORMAT_D16_UNORM_S8_UINT = 128
    VK_FORMAT_D24_UNORM_S8_UINT = 129
    VK_FORMAT_D32_SFLOAT_S8_UINT = 130
    VK_FORMAT_BC1_RGB_UNORM_BLOCK = 131
    VK_FORMAT_BC1_RGB_SRGB_BLOCK = 132
    VK_FORMAT_BC1_RGBA_UNORM_BLOCK = 133
    VK_FORMAT_BC1_RGBA_SRGB_BLOCK = 134
    VK_FORMAT_BC2_UNORM_BLOCK = 135
    VK_FORMAT_BC2_SRGB_BLOCK = 136
    VK_FORMAT_BC3_UNORM_BLOCK = 137
    VK_FORMAT_BC3_SRGB_BLOCK = 138
    VK_FORMAT_BC4_UNORM_BLOCK = 139
    VK_FORMAT_BC4_SNORM_BLOCK = 140
    VK_FORMAT_BC5_UNORM_BLOCK = 141
    VK_FORMAT_BC5_SNORM_BLOCK = 142
    VK_FORMAT_BC6H_UFLOAT_BLOCK = 143
    VK_FORMAT_BC6H_SFLOAT_BLOCK = 144
    VK_FORMAT_BC7_UNORM_BLOCK = 145
    VK_FORMAT_BC7_SRGB_BLOCK = 146
    VK_FORMAT_ETC2_R8G8B8_UNORM_BLOCK = 147
    VK_FORMAT_ETC2_R8G8B8_SRGB_BLOCK = 148
    VK_FORMAT_ETC2_R8G8B8A1_UNORM_BLOCK = 149
    VK_FORMAT_ETC2_R8G8B8A1_SRGB_BLOCK = 150
    VK_FORMAT_ETC2_R8G8B8A8_UNORM_BLOCK = 151
    VK_FORMAT_ETC2_R8G8B8A8_SRGB_BLOCK = 152
    VK_FORMAT_EAC_R11_UNORM_BLOCK = 153
    VK_FORMAT_EAC_R11_SNORM_BLOCK = 154
    VK_FORMAT_EAC_R11G11_UNORM_BLOCK = 155
    VK_FORMAT_EAC_R11G11_SNORM_BLOCK = 156
    VK_FORMAT_ASTC_4x4_UNORM_BLOCK = 157
    VK_FORMAT_ASTC_4x4_SRGB_BLOCK = 158
    VK_FORMAT_ASTC_5x4_UNORM_BLOCK = 159
    VK_FORMAT_ASTC_5x4_SRGB_BLOCK = 160
    VK_FORMAT_ASTC_5x5_UNORM_BLOCK = 161
    VK_FORMAT_ASTC_5x5_SRGB_BLOCK = 162
    VK_FORMAT_ASTC_6x5_UNORM_BLOCK = 163
    VK_FORMAT_ASTC_6x5_SRGB_BLOCK = 164
    VK_FORMAT_ASTC_6x6_UNORM_BLOCK = 165
    VK_FORMAT_ASTC_6x6_SRGB_BLOCK = 166
    VK_FORMAT_ASTC_8x5_UNORM_BLOCK = 167
    VK_FORMAT_ASTC_8x5_SRGB_BLOCK = 168
    VK_FORMAT_ASTC_8x6_UNORM_BLOCK = 169
    VK_FORMAT_ASTC_8x6_SRGB_BLOCK = 170
    VK_FORMAT_ASTC_8x8_UNORM_BLOCK = 171
    VK_FORMAT_ASTC_8x8_SRGB_BLOCK = 172
    VK_FORMAT_ASTC_10x5_UNORM_BLOCK = 173
    VK_FORMAT_ASTC_10x5_SRGB_BLOCK = 174
    VK_FORMAT_ASTC_10x6_UNORM_BLOCK = 175
    VK_FORMAT_ASTC_10x6_SRGB_BLOCK = 176
    VK_FORMAT_ASTC_10x8_UNORM_BLOCK = 177
    VK_FORMAT_ASTC_10x8_SRGB_BLOCK = 178
    VK_FORMAT_ASTC_10x10_UNORM_BLOCK = 179
    VK_FORMAT_ASTC_10x10_SRGB_BLOCK = 180
    VK_FORMAT_ASTC_12x10_UNORM_BLOCK = 181
    VK_FORMAT_ASTC_12x10_SRGB_BLOCK = 182
    VK_FORMAT_ASTC_12x12_UNORM_BLOCK = 183
    VK_FORMAT_ASTC_12x12_SRGB_BLOCK = 184
    # Provided by VK_VERSION_1_1
    VK_FORMAT_G8B8G8R8_422_UNORM = 1000156000
    # Provided by VK_VERSION_1_1
    VK_FORMAT_B8G8R8G8_422_UNORM = 1000156001
    # Provided by VK_VERSION_1_1
    VK_FORMAT_G8_B8_R8_3PLANE_420_UNORM = 1000156002
    # Provided by VK_VERSION_1_1
    VK_FORMAT_G8_B8R8_2PLANE_420_UNORM = 1000156003
    # Provided by VK_VERSION_1_1
    VK_FORMAT_G8_B8_R8_3PLANE_422_UNORM = 1000156004
    # Provided by VK_VERSION_1_1
    VK_FORMAT_G8_B8R8_2PLANE_422_UNORM = 1000156005
    # Provided by VK_VERSION_1_1
    VK_FORMAT_G8_B8_R8_3PLANE_444_UNORM = 1000156006
    # Provided by VK_VERSION_1_1
    VK_FORMAT_R10X6_UNORM_PACK16 = 1000156007
    # Provided by VK_VERSION_1_1
    VK_FORMAT_R10X6G10X6_UNORM_2PACK16 = 1000156008
    # Provided by VK_VERSION_1_1
    VK_FORMAT_R10X6G10X6B10X6A10X6_UNORM_4PACK16 = 1000156009
    # Provided by VK_VERSION_1_1
    VK_FORMAT_G10X6B10X6G10X6R10X6_422_UNORM_4PACK16 = 1000156010
    # Provided by VK_VERSION_1_1
    VK_FORMAT_B10X6G10X6R10X6G10X6_422_UNORM_4PACK16 = 1000156011
    # Provided by VK_VERSION_1_1
    VK_FORMAT_G10X6_B10X6_R10X6_3PLANE_420_UNORM_3PACK16 = 1000156012
    # Provided by VK_VERSION_1_1
    VK_FORMAT_G10X6_B10X6R10X6_2PLANE_420_UNORM_3PACK16 = 1000156013
    # Provided by VK_VERSION_1_1
    VK_FORMAT_G10X6_B10X6_R10X6_3PLANE_422_UNORM_3PACK16 = 1000156014
    # Provided by VK_VERSION_1_1
    VK_FORMAT_G10X6_B10X6R10X6_2PLANE_422_UNORM_3PACK16 = 1000156015
    # Provided by VK_VERSION_1_1
    VK_FORMAT_G10X6_B10X6_R10X6_3PLANE_444_UNORM_3PACK16 = 1000156016
    # Provided by VK_VERSION_1_1
    VK_FORMAT_R12X4_UNORM_PACK16 = 1000156017
    # Provided by VK_VERSION_1_1
    VK_FORMAT_R12X4G12X4_UNORM_2PACK16 = 1000156018
    # Provided by VK_VERSION_1_1
    VK_FORMAT_R12X4G12X4B12X4A12X4_UNORM_4PACK16 = 1000156019
    # Provided by VK_VERSION_1_1
    VK_FORMAT_G12X4B12X4G12X4R12X4_422_UNORM_4PACK16 = 1000156020
    # Provided by VK_VERSION_1_1
    VK_FORMAT_B12X4G12X4R12X4G12X4_422_UNORM_4PACK16 = 1000156021
    # Provided by VK_VERSION_1_1
    VK_FORMAT_G12X4_B12X4_R12X4_3PLANE_420_UNORM_3PACK16 = 1000156022
    # Provided by VK_VERSION_1_1
    VK_FORMAT_G12X4_B12X4R12X4_2PLANE_420_UNORM_3PACK16 = 1000156023
    # Provided by VK_VERSION_1_1
    VK_FORMAT_G12X4_B12X4_R12X4_3PLANE_422_UNORM_3PACK16 = 1000156024
    # Provided by VK_VERSION_1_1
    VK_FORMAT_G12X4_B12X4R12X4_2PLANE_422_UNORM_3PACK16 = 1000156025
    # Provided by VK_VERSION_1_1
    VK_FORMAT_G12X4_B12X4_R12X4_3PLANE_444_UNORM_3PACK16 = 1000156026
    # Provided by VK_VERSION_1_1
    VK_FORMAT_G16B16G16R16_422_UNORM = 1000156027
    # Provided by VK_VERSION_1_1
    VK_FORMAT_B16G16R16G16_422_UNORM = 1000156028
    # Provided by VK_VERSION_1_1
    VK_FORMAT_G16_B16_R16_3PLANE_420_UNORM = 1000156029
    # Provided by VK_VERSION_1_1
    VK_FORMAT_G16_B16R16_2PLANE_420_UNORM = 1000156030
    # Provided by VK_VERSION_1_1
    VK_FORMAT_G16_B16_R16_3PLANE_422_UNORM = 1000156031
    # Provided by VK_VERSION_1_1
    VK_FORMAT_G16_B16R16_2PLANE_422_UNORM = 1000156032
    # Provided by VK_VERSION_1_1
    VK_FORMAT_G16_B16_R16_3PLANE_444_UNORM = 1000156033
    # Provided by VK_IMG_format_pvrtc
    VK_FORMAT_PVRTC1_2BPP_UNORM_BLOCK_IMG = 1000054000
    # Provided by VK_IMG_format_pvrtc
    VK_FORMAT_PVRTC1_4BPP_UNORM_BLOCK_IMG = 1000054001
    # Provided by VK_IMG_format_pvrtc
    VK_FORMAT_PVRTC2_2BPP_UNORM_BLOCK_IMG = 1000054002
    # Provided by VK_IMG_format_pvrtc
    VK_FORMAT_PVRTC2_4BPP_UNORM_BLOCK_IMG = 1000054003
    # Provided by VK_IMG_format_pvrtc
    VK_FORMAT_PVRTC1_2BPP_SRGB_BLOCK_IMG = 1000054004
    # Provided by VK_IMG_format_pvrtc
    VK_FORMAT_PVRTC1_4BPP_SRGB_BLOCK_IMG = 1000054005
    # Provided by VK_IMG_format_pvrtc
    VK_FORMAT_PVRTC2_2BPP_SRGB_BLOCK_IMG = 1000054006
    # Provided by VK_IMG_format_pvrtc
    VK_FORMAT_PVRTC2_4BPP_SRGB_BLOCK_IMG = 1000054007
    # Provided by VK_EXT_texture_compression_astc_hdr
    VK_FORMAT_ASTC_4x4_SFLOAT_BLOCK_EXT = 1000066000
    # Provided by VK_EXT_texture_compression_astc_hdr
    VK_FORMAT_ASTC_5x4_SFLOAT_BLOCK_EXT = 1000066001
    # Provided by VK_EXT_texture_compression_astc_hdr
    VK_FORMAT_ASTC_5x5_SFLOAT_BLOCK_EXT = 1000066002
    # Provided by VK_EXT_texture_compression_astc_hdr
    VK_FORMAT_ASTC_6x5_SFLOAT_BLOCK_EXT = 1000066003
    # Provided by VK_EXT_texture_compression_astc_hdr
    VK_FORMAT_ASTC_6x6_SFLOAT_BLOCK_EXT = 1000066004
    # Provided by VK_EXT_texture_compression_astc_hdr
    VK_FORMAT_ASTC_8x5_SFLOAT_BLOCK_EXT = 1000066005
    # Provided by VK_EXT_texture_compression_astc_hdr
    VK_FORMAT_ASTC_8x6_SFLOAT_BLOCK_EXT = 1000066006
    # Provided by VK_EXT_texture_compression_astc_hdr
    VK_FORMAT_ASTC_8x8_SFLOAT_BLOCK_EXT = 1000066007
    # Provided by VK_EXT_texture_compression_astc_hdr
    VK_FORMAT_ASTC_10x5_SFLOAT_BLOCK_EXT = 1000066008
    # Provided by VK_EXT_texture_compression_astc_hdr
    VK_FORMAT_ASTC_10x6_SFLOAT_BLOCK_EXT = 1000066009
    # Provided by VK_EXT_texture_compression_astc_hdr
    VK_FORMAT_ASTC_10x8_SFLOAT_BLOCK_EXT = 1000066010
    # Provided by VK_EXT_texture_compression_astc_hdr
    VK_FORMAT_ASTC_10x10_SFLOAT_BLOCK_EXT = 1000066011
    # Provided by VK_EXT_texture_compression_astc_hdr
    VK_FORMAT_ASTC_12x10_SFLOAT_BLOCK_EXT = 1000066012
    # Provided by VK_EXT_texture_compression_astc_hdr
    VK_FORMAT_ASTC_12x12_SFLOAT_BLOCK_EXT = 1000066013
    # Provided by VK_EXT_ycbcr_2plane_444_formats
    VK_FORMAT_G8_B8R8_2PLANE_444_UNORM_EXT = 1000330000
    # Provided by VK_EXT_ycbcr_2plane_444_formats
    VK_FORMAT_G10X6_B10X6R10X6_2PLANE_444_UNORM_3PACK16_EXT = 1000330001
    # Provided by VK_EXT_ycbcr_2plane_444_formats
    VK_FORMAT_G12X4_B12X4R12X4_2PLANE_444_UNORM_3PACK16_EXT = 1000330002
    # Provided by VK_EXT_ycbcr_2plane_444_formats
    VK_FORMAT_G16_B16R16_2PLANE_444_UNORM_EXT = 1000330003
    # Provided by VK_EXT_4444_formats
    VK_FORMAT_A4R4G4B4_UNORM_PACK16_EXT = 1000340000
    # Provided by VK_EXT_4444_formats
    VK_FORMAT_A4B4G4R4_UNORM_PACK16_EXT = 1000340001
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_G8B8G8R8_422_UNORM_KHR = VK_FORMAT_G8B8G8R8_422_UNORM
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_B8G8R8G8_422_UNORM_KHR = VK_FORMAT_B8G8R8G8_422_UNORM
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_G8_B8_R8_3PLANE_420_UNORM_KHR = VK_FORMAT_G8_B8_R8_3PLANE_420_UNORM
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_G8_B8R8_2PLANE_420_UNORM_KHR = VK_FORMAT_G8_B8R8_2PLANE_420_UNORM
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_G8_B8_R8_3PLANE_422_UNORM_KHR = VK_FORMAT_G8_B8_R8_3PLANE_422_UNORM
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_G8_B8R8_2PLANE_422_UNORM_KHR = VK_FORMAT_G8_B8R8_2PLANE_422_UNORM
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_G8_B8_R8_3PLANE_444_UNORM_KHR = VK_FORMAT_G8_B8_R8_3PLANE_444_UNORM
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_R10X6_UNORM_PACK16_KHR = VK_FORMAT_R10X6_UNORM_PACK16
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_R10X6G10X6_UNORM_2PACK16_KHR = VK_FORMAT_R10X6G10X6_UNORM_2PACK16
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_R10X6G10X6B10X6A10X6_UNORM_4PACK16_KHR = VK_FORMAT_R10X6G10X6B10X6A10X6_UNORM_4PACK16
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_G10X6B10X6G10X6R10X6_422_UNORM_4PACK16_KHR = VK_FORMAT_G10X6B10X6G10X6R10X6_422_UNORM_4PACK16
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_B10X6G10X6R10X6G10X6_422_UNORM_4PACK16_KHR = VK_FORMAT_B10X6G10X6R10X6G10X6_422_UNORM_4PACK16
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_G10X6_B10X6_R10X6_3PLANE_420_UNORM_3PACK16_KHR = VK_FORMAT_G10X6_B10X6_R10X6_3PLANE_420_UNORM_3PACK16
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_G10X6_B10X6R10X6_2PLANE_420_UNORM_3PACK16_KHR = VK_FORMAT_G10X6_B10X6R10X6_2PLANE_420_UNORM_3PACK16
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_G10X6_B10X6_R10X6_3PLANE_422_UNORM_3PACK16_KHR = VK_FORMAT_G10X6_B10X6_R10X6_3PLANE_422_UNORM_3PACK16
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_G10X6_B10X6R10X6_2PLANE_422_UNORM_3PACK16_KHR = VK_FORMAT_G10X6_B10X6R10X6_2PLANE_422_UNORM_3PACK16
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_G10X6_B10X6_R10X6_3PLANE_444_UNORM_3PACK16_KHR = VK_FORMAT_G10X6_B10X6_R10X6_3PLANE_444_UNORM_3PACK16
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_R12X4_UNORM_PACK16_KHR = VK_FORMAT_R12X4_UNORM_PACK16
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_R12X4G12X4_UNORM_2PACK16_KHR = VK_FORMAT_R12X4G12X4_UNORM_2PACK16
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_R12X4G12X4B12X4A12X4_UNORM_4PACK16_KHR = VK_FORMAT_R12X4G12X4B12X4A12X4_UNORM_4PACK16
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_G12X4B12X4G12X4R12X4_422_UNORM_4PACK16_KHR = VK_FORMAT_G12X4B12X4G12X4R12X4_422_UNORM_4PACK16
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_B12X4G12X4R12X4G12X4_422_UNORM_4PACK16_KHR = VK_FORMAT_B12X4G12X4R12X4G12X4_422_UNORM_4PACK16
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_G12X4_B12X4_R12X4_3PLANE_420_UNORM_3PACK16_KHR = VK_FORMAT_G12X4_B12X4_R12X4_3PLANE_420_UNORM_3PACK16
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_G12X4_B12X4R12X4_2PLANE_420_UNORM_3PACK16_KHR = VK_FORMAT_G12X4_B12X4R12X4_2PLANE_420_UNORM_3PACK16
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_G12X4_B12X4_R12X4_3PLANE_422_UNORM_3PACK16_KHR = VK_FORMAT_G12X4_B12X4_R12X4_3PLANE_422_UNORM_3PACK16
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_G12X4_B12X4R12X4_2PLANE_422_UNORM_3PACK16_KHR = VK_FORMAT_G12X4_B12X4R12X4_2PLANE_422_UNORM_3PACK16
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_G12X4_B12X4_R12X4_3PLANE_444_UNORM_3PACK16_KHR = VK_FORMAT_G12X4_B12X4_R12X4_3PLANE_444_UNORM_3PACK16
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_G16B16G16R16_422_UNORM_KHR = VK_FORMAT_G16B16G16R16_422_UNORM
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_B16G16R16G16_422_UNORM_KHR = VK_FORMAT_B16G16R16G16_422_UNORM
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_G16_B16_R16_3PLANE_420_UNORM_KHR = VK_FORMAT_G16_B16_R16_3PLANE_420_UNORM
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_G16_B16R16_2PLANE_420_UNORM_KHR = VK_FORMAT_G16_B16R16_2PLANE_420_UNORM
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_G16_B16_R16_3PLANE_422_UNORM_KHR = VK_FORMAT_G16_B16_R16_3PLANE_422_UNORM
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_G16_B16R16_2PLANE_422_UNORM_KHR = VK_FORMAT_G16_B16R16_2PLANE_422_UNORM
    # Provided by VK_KHR_sampler_ycbcr_conversion
    VK_FORMAT_G16_B16_R16_3PLANE_444_UNORM_KHR = VK_FORMAT_G16_B16_R16_3PLANE_444_UNORM


class SupercompressionScheme(Enum):
    NONE = 0
    BasisLZ = 1
    Zstandard = 2
    ZLIB = 3


class Const:
    # IDENTIFIER = bytes((0xAB,0x4B,0x54,0x58,0x20,0x32,0x30,0xBB,0x0D,0x0A,0x1A,0x0A))
    IDENTIFIER = b'\xABKTX 20\xBB\r\n\x1A\n'
    ENDIAN_COMPATIBLE = bytes((0x04, 0x03, 0x02, 0x01))
    ENDIAN_INCOMPATIBLE = bytes((0x01, 0x02, 0x03, 0x04))


class KtxError(RuntimeError):
    pass


class BytesReader:
    def __init__(self, data: bytes) -> None:
        self.data = data
        self.pos = 0

    def is_end(self) -> bool:
        return self.pos >= len(self.data)

    def get_padding_size(self, alignment: int) -> int:
        mod = self.pos % 8
        if mod == 0:
            return 0
        return alignment-mod

    def read(self, size: int) -> bytes:
        if size == 0:
            return b''
        if self.pos+size > len(self.data):
            raise IOError()
        data = self.data[self.pos:self.pos+size]
        self.pos += size
        return data

    def read_int32(self) -> int:
        data = self.read(4)
        return struct.unpack('i', data)[0]

    def read_uint16(self) -> int:
        data = self.read(2)
        return struct.unpack('H', data)[0]

    def read_uint32(self) -> int:
        data = self.read(4)
        return struct.unpack('I', data)[0]

    def read_uint64(self) -> int:
        data = self.read(8)
        return struct.unpack('Q', data)[0]


class LevelIndex(NamedTuple):
    byteOffset: int
    byteLength: int
    uncompressedByteLength: int


class Ktx2(NamedTuple):
    vkFormat: VkFormat
    typeSize: int
    pixelWidth: int
    pixelHeight: int
    pixelDepth: int
    layerCount: int
    faceCount: int
    levelCount: int
    supercompressionScheme: SupercompressionScheme

    dfdByteOffset: int
    dfdByteLength: int
    kvdByteOffset: int
    kvdByteLength: int
    sgdByteOffset: int
    sgdByteLength: int

    levelIndices: List[LevelIndex]

    dfd: Any

    kv: Dict[str, bytes]

    supercompressionGlobalData: bytes

    levelImages: List[Any]


class DFDBasicFlags(NamedTuple):
    colorModel: int
    colorPrimaries: int
    transferFunction: int
    flags: int
    texelBlockDimension0: int
    texelBlockDimension1: int
    texelBlockDimension2: int
    texelBlockDimension3: int
    bytesPlane0: int
    bytesPlane1: int
    bytesPlane2: int
    bytesPlane3: int
    bytesPlane4: int
    bytesPlane5: int
    bytesPlane6: int
    bytesPlane7: int


def parse_dfd(data: bytes):
    r = BytesReader(data)
    dfdTotalSize = r.read_uint32()
    descriptorType_vendorId = r.read_uint32()
    if descriptorType_vendorId != 0:
        raise NotImplementedError()
    versionNumber = r.read_uint16()
    descriptorBlockSize = r.read_uint16()
    match descriptorType_vendorId:
        case 0:
            # Basic
            dfd = DFDBasicFlags(*r.read(16))
            sample_count = (descriptorBlockSize - 24)//16
            samples = [r.read(16) for _ in range(sample_count)]
            return dfd, samples

        case _:
            raise NotImplementedError()


class Image(NamedTuple):
    data: bytes
    width: int
    height: int


class CubeMap(NamedTuple):
    x_positive: Image
    x_negative: Image
    y_positive: Image
    y_negative: Image
    z_positive: Image
    z_negative: Image


def get_stride(format: VkFormat) -> int:
    match format:
        case VkFormat.VK_FORMAT_R16G16B16A16_SFLOAT:
            return 8
        case _:
            raise NotImplementedError()


def parse_cubemap(level: int, data: bytes, width: int, height: int, format: VkFormat) -> CubeMap:

    stride = get_stride(format)

    factor = 1
    if level > 0:
        factor = pow(2, level)

    width = width//factor
    height = height//factor
    image_size = width * height * stride
    assert image_size * 6 == len(data)

    r = BytesReader(data)
    cubemap = CubeMap(
        *[Image(r.read(image_size), width, height) for _ in range(6)])
    return cubemap


def parse_bytes(data: bytes) -> Ktx2:
    r = BytesReader(data)
    match r.read(12):
        case Const.IDENTIFIER:
            pass
        case _:
            raise KtxError('invalid identifier')

    vkFormat = VkFormat(r.read_uint32())
    typeSize = r.read_uint32()
    pixelWidth = r.read_uint32()
    pixelHeight = r.read_uint32()
    pixelDepth = r.read_uint32()
    layerCount = r.read_uint32()
    faceCount = r.read_uint32()
    levelCount = r.read_uint32()
    supercompressionScheme = SupercompressionScheme(r.read_uint32())

    # Index
    dfdByteOffset = r.read_uint32()
    dfdByteLength = r.read_uint32()
    kvdByteOffset = r.read_uint32()
    kvdByteLength = r.read_uint32()
    sgdByteOffset = r.read_uint64()
    sgdByteLength = r.read_uint64()

    # Level Index
    levelIndices = [LevelIndex(r.read_uint64(), r.read_uint64(), r.read_uint64())
                    for _ in range(levelCount)]

    # Data Format Descriptor
    dfd, samples = parse_dfd(r.read(dfdByteLength))

    # Key/Value Data
    assert r.pos == kvdByteOffset
    # skip
    # r.read(kvdByteLength)
    kvdEnd = kvdByteOffset + kvdByteLength
    kv: Dict[str, bytes] = {}
    while r.pos < kvdEnd:
        keyAndValueByteLength = r.read_uint32()
        if keyAndValueByteLength >= 2:
            keyAndValue = r.read(keyAndValueByteLength)
            pos = keyAndValue.find(0)
            key = keyAndValue[:pos].decode('utf-8')
            kv[key] = keyAndValue[pos+1:]
        # skip padding
        padding = r.get_padding_size(4)
        _ = r.read(padding)

    if (sgdByteLength > 0):
        # skip padding
        padding = r.get_padding_size(8)
        _ = r.read(padding)

    # Supercompression Global Data
    supercompressionGlobalData = r.read(sgdByteLength)

    # Mip Level Array
    if levelCount == 0:
        levelCount = 1
    if layerCount == 0:
        layerCount = 1
    if pixelDepth == 0:
        pixelDepth = 1
    match layerCount, pixelDepth:
        case 1, 1:
            if faceCount == 6:
                levelImages = []
                for level in range(levelCount):
                    level_width = pixelWidth
                    level_height = pixelHeight
                    levelImages.append(parse_cubemap(level,
                                                     r.read(levelIndices[level].byteLength), level_width, level_height, vkFormat))

            else:
                raise NotImplementedError()
        case _:
            raise NotImplementedError()

    assert r.is_end()

    return Ktx2(
        vkFormat,
        typeSize,
        pixelWidth,
        pixelHeight,
        pixelDepth,
        layerCount,
        faceCount,
        levelCount,
        supercompressionScheme,
        dfdByteOffset,
        dfdByteLength,
        kvdByteOffset,
        kvdByteLength,
        sgdByteOffset,
        sgdByteLength,
        levelIndices,
        (dfd, samples),
        kv,
        supercompressionGlobalData,
        levelImages)


def parse_path(path: pathlib.Path) -> Ktx2:
    return parse_bytes(path.read_bytes())
