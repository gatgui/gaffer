##########################################################################
#
#  Copyright (c) 2011-2012, Image Engine Design Inc. All rights reserved.
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

import sys
import traceback

import IECore

import GafferUI

class ErrorDialogue( GafferUI.Dialogue ) :

	# Constructs a dialogue to display errors specified by any combination of the
	# following arguments :
	#
	#  - message : A simple (string) message to display.
	#  - messages : A list of messages in the format stored by `IECore.CapturingMessageHandler.messages`
	#  - details : A string containing additional details to be shown in a collapsed section.
	def __init__( self, title, message = None, details = None, messages = None, closeLabel = "Close", **kw ) :

		GafferUI.Dialogue.__init__( self, title, sizeMode=GafferUI.Window.SizeMode.Manual, **kw )

		with GafferUI.ListContainer( GafferUI.ListContainer.Orientation.Vertical, spacing = 8 ) as column :

			GafferUI.Image(
				"failure.png",
				parenting = {
					"horizontalAlignment" : GafferUI.HorizontalAlignment.Center,
					"expand" : True,
				}
			)

			GafferUI.Spacer( IECore.V2i( 250, 1 ) )

			if message is not None :
				GafferUI.Label(
					"<b>" + IECore.StringUtil.wrap( message, 60 ).replace( "\n", "<br>" ) + "</b>",
					parenting = {
						"horizontalAlignment" : GafferUI.HorizontalAlignment.Center
					}
				)

			if messages is not None :
				messageWidget = GafferUI.MessageWidget()
				for m in messages :
					messageWidget.messageHandler().handle( m.level, m.context, m.message )

			if details is not None :
				with GafferUI.Collapsible( label = "Details", collapsed = True ) :
					GafferUI.MultiLineTextWidget(
						text = details,
						editable = False,
					)

		self._setWidget( column )

		self.__closeButton = self._addButton( closeLabel )

	## A context manager which displays a modal ErrorDialogue if an exception is
	# caught or any warning or error messages are emitted via IECore.MessageHandler.
	class ErrorHandler( IECore.MessageHandler ) :

		def __init__(
			self,
			handleExceptions = True,
			handleErrorMessages = True,
			handleWarningMessages = True,
			parentWindow = None, # Passed to waitForButton()
			**kw # Passed to the ErrorDialogue constructor
		) :

			IECore.MessageHandler.__init__( self )

			self.__handleExceptions = handleExceptions
			self.__handleErrorMessages = handleErrorMessages
			self.__handleWarningMessages = handleWarningMessages
			self.__parentWindow = parentWindow
			self.__kw = kw

			self.__originalMessageHandler = None
			self.__capturingMessageHandler = IECore.CapturingMessageHandler()

		def handle( self, level, context, message ) :

			handler = self.__originalMessageHandler

			if (
				( level == self.Level.Error and self.__handleErrorMessages ) or
				( level == self.Level.Warning and self.__handleWarningMessages )
			) :
				handler = self.__capturingMessageHandler

			handler.handle( level, context, message )

		def __enter__( self ) :

			self.__originalMessageHandler = IECore.MessageHandler.currentHandler()
			IECore.MessageHandler.__enter__( self )

		def __exit__( self, type, value, traceback ) :

			IECore.MessageHandler.__exit__( self, type, value, traceback )
			self.__originalMessageHandler = None

			result = False
			if type is not None and self.__handleExceptions :
				self.__capturingMessageHandler.handle( self.Level.Error, self.__kw.get( "title", "Error" ), str( value ) )
				result = True

			if len( self.__capturingMessageHandler.messages ) :
				self.__kw["messages"] = self.__capturingMessageHandler.messages
				ErrorDialogue( **self.__kw ).waitForButton( parentWindow = self.__parentWindow )

			return result

	## Displays an exception in a modal dialogue. By default the currently handled exception is displayed
	# but another exception can be displayed by specifying excInfo in the same format as returned by sys.exc_info()
	@staticmethod
	def displayException( title="Error", messagePrefix=None, withDetails=True, parentWindow=None, exceptionInfo=None ) :

		if exceptionInfo is None :
			exceptionInfo = sys.exc_info()

		if exceptionInfo[0] is None :
			return

		message = str( exceptionInfo[1] )
		if messagePrefix :
			message = messagePrefix + message

		if withDetails :
			details = "".join( traceback.format_exception( *exceptionInfo ) )
		else :
			details = False

		dialogue = ErrorDialogue(
			title = title,
			message = message,
			details = details,
		)

		dialogue.waitForButton( parentWindow=parentWindow )

	## A simple context manager which calls displayException() if any exceptions are caught.
	class ExceptionHandler( object ) :

		## The keyword arguments will be passed to displayException().
		def __init__( self, **kw ) :

			self.__kw = kw

		def __enter__( self ) :

			pass

		def __exit__( self, type, value, traceback ) :

			if type is not None :
				ErrorDialogue.displayException( exceptionInfo=( type, value, traceback ), **self.__kw )
				return True
