// BSD 3-Clause License Copyright (c) 2022, Pierre Delaunay All rights reserved.

#include "GKML.h"

#define LOCTEXT_NAMESPACE "FGKMLModule"

void FGKMLModule::StartupModule()
{
	// This code will execute after your module is loaded into memory; the exact timing is specified in the .uplugin file per-module
}

void FGKMLModule::ShutdownModule()
{
	// This function may be called during shutdown to clean up your module.  For modules that support dynamic reloading,
	// we call this function before unloading the module.
}

#undef LOCTEXT_NAMESPACE
	
IMPLEMENT_MODULE(FGKMLModule, GKML)