// BSD 3-Clause License Copyright (c) 2022, Pierre Delaunay All rights reserved.

#pragma once

// Unreal Engine
#include "CoreMinimal.h"
#include "Modules/ModuleManager.h"

class FGKMLModule : public IModuleInterface
{
public:

	/** IModuleInterface implementation */
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;
};
