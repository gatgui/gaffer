##########################################################################
#
#  Copyright (c) 2015, Image Engine Design Inc. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#      * Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#
#      * Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided with
#        the distribution.
#
#      * Neither the name of John Haddon nor the names of
#        any other contributors to this software may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##########################################################################

import itertools

import Gaffer
import GafferImage

Gaffer.Metadata.registerNode(

	GafferImage.Resample,

	"description",
	"""
	Utility node used internally within GafferImage, but
	not intended to be used directly by end users.
	""",

	plugs = {

		"matrix" : [

			"description",
			"""
			The transform to be applied to the input image.
			This must contain only translation and scaling.
			""",

		],

		"filter" : [

			"description",
			"""
			The filter used to perform the resampling. The name
			of any OIIO filter may be specified. The default automatically
			picks an appropriate high-quality filter based on whether
			or not the image is being enlarged or reduced.
			""",

			"plugValueWidget:type", "GafferUI.PresetsPlugValueWidget",

			"preset:Default", "",

		] + list( itertools.chain(

			*[ ( "preset:" + x.title(), x ) for x in GafferImage.Resample.filters() ]

		) ),

		"filterWidth" : [

			"description",
			"""
			An override for the width of the filter used. This is
			specified as a number of pixels in the output image. The
			default value of 0 causes a good default width to be
			picked based on the filter type.
			""",

		],

		"boundingMode" : [

			"description",
			"""
			The method used when a filter references pixels outside the
			input data window.
			""",

			"preset:Black", GafferImage.Sampler.BoundingMode.Black,
			"preset:Clamp", GafferImage.Sampler.BoundingMode.Clamp,

			"plugValueWidget:type", "GafferUI.PresetsPlugValueWidget",

		],

		"expandDataWindow" : [

			"description",
			"""
			Expands the data window by the filter radius, to include the
			external pixels affected by the filter.
			""",

		],

		"debug" : [


			"description",
			"""
			Enables debug output. The HorizontalPass setting outputs
			an intermediate image filtered just in the horizontal
			direction - this is an internal optimisation used when
			filtering with a separable filter. The SinglePass setting
			forces all filtering to be done in a single pass (as if
			the filter was non-separable) and can be used for validating
			the results of the the two-pass (default) approach.
			""",

			"preset:Off", GafferImage.Resample.Debug.Off,
			"preset:HorizontalPass", GafferImage.Resample.Debug.HorizontalPass,
			"preset:SinglePass", GafferImage.Resample.Debug.SinglePass,

			"plugValueWidget:type", "GafferUI.PresetsPlugValueWidget",

		],

	}

)
