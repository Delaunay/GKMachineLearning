// BSD 3-Clause License Copyright (c) 2022, Pierre Delaunay All rights reserved.

#pragma once

// Unreal
#include "CoreMinimal.h"
#include "GameFramework/PlayerState.h"

// Generated
#include "GKMLPlayerState.generated.h"

/**
 *
 */
UCLASS(Blueprintable, BlueprintType)
class GKML_API AGKMLPlayerState : public APlayerState
{
	GENERATED_BODY()

public:

	//! Expose SetScore to blueprint so we can implement a custom reward function
	UFUNCTION(BlueprintCallable, Category = Score)
	void K2_SetScore(const float value) {
		SetScore(value);
	}
};
