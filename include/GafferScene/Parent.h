//////////////////////////////////////////////////////////////////////////
//
//  Copyright (c) 2014, Image Engine Design Inc. All rights reserved.
//
//  Redistribution and use in source and binary forms, with or without
//  modification, are permitted provided that the following conditions are
//  met:
//
//      * Redistributions of source code must retain the above
//        copyright notice, this list of conditions and the following
//        disclaimer.
//
//      * Redistributions in binary form must reproduce the above
//        copyright notice, this list of conditions and the following
//        disclaimer in the documentation and/or other materials provided with
//        the distribution.
//
//      * Neither the name of John Haddon nor the names of
//        any other contributors to this software may be used to endorse or
//        promote products derived from this software without specific prior
//        written permission.
//
//  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
//  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
//  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
//  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
//  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
//  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
//  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
//  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
//  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
//  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
//  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
//////////////////////////////////////////////////////////////////////////

#ifndef GAFFERSCENE_PARENT_H
#define GAFFERSCENE_PARENT_H

#include "GafferScene/BranchCreator.h"

namespace GafferScene
{

class Parent : public BranchCreator
{

	public :

		Parent( const std::string &name=defaultName<Parent>() );
		virtual ~Parent();

		IE_CORE_DECLARERUNTIMETYPEDEXTENSION( GafferScene::Parent, ParentTypeId, BranchCreator );

		ScenePlug *childPlug();
		const ScenePlug *childPlug() const;

		virtual void affects( const Gaffer::Plug *input, AffectedPlugsContainer &outputs ) const;

	protected :

		virtual void hashBranchBound( const ScenePath &parentPath, const ScenePath &branchPath, const Gaffer::Context *context, IECore::MurmurHash &h ) const;
		virtual Imath::Box3f computeBranchBound( const ScenePath &parentPath, const ScenePath &branchPath, const Gaffer::Context *context ) const;

		virtual void hashBranchTransform( const ScenePath &parentPath, const ScenePath &branchPath, const Gaffer::Context *context, IECore::MurmurHash &h ) const;
		virtual Imath::M44f computeBranchTransform( const ScenePath &parentPath, const ScenePath &branchPath, const Gaffer::Context *context ) const;

		virtual void hashBranchAttributes( const ScenePath &parentPath, const ScenePath &branchPath, const Gaffer::Context *context, IECore::MurmurHash &h ) const;
		virtual IECore::ConstCompoundObjectPtr computeBranchAttributes( const ScenePath &parentPath, const ScenePath &branchPath, const Gaffer::Context *context ) const;

		virtual void hashBranchObject( const ScenePath &parentPath, const ScenePath &branchPath, const Gaffer::Context *context, IECore::MurmurHash &h ) const;
		virtual IECore::ConstObjectPtr computeBranchObject( const ScenePath &parentPath, const ScenePath &branchPath, const Gaffer::Context *context ) const;

		virtual void hashBranchChildNames( const ScenePath &parentPath, const ScenePath &branchPath, const Gaffer::Context *context, IECore::MurmurHash &h ) const;
		virtual IECore::ConstInternedStringVectorDataPtr computeBranchChildNames( const ScenePath &parentPath, const ScenePath &branchPath, const Gaffer::Context *context ) const;

		virtual void hashBranchSetNames( const ScenePath &parentPath, const Gaffer::Context *context, IECore::MurmurHash &h ) const;
		virtual IECore::ConstInternedStringVectorDataPtr computeBranchSetNames( const ScenePath &parentPath, const Gaffer::Context *context ) const;

		virtual void hashBranchSet( const ScenePath &parentPath, const IECore::InternedString &setName, const Gaffer::Context *context, IECore::MurmurHash &h ) const;
		virtual GafferScene::ConstPathMatcherDataPtr computeBranchSet( const ScenePath &parentPath, const IECore::InternedString &setName, const Gaffer::Context *context ) const;

	private :

		static size_t g_firstPlugIndex;

};

IE_CORE_DECLAREPTR( Parent )

} // namespace GafferScene

#endif // GAFFERSCENE_PARENT_H
