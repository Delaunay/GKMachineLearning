// BSD 3-Clause License Copyright (c) 2022, Pierre Delaunay All rights reserved.

#pragma once

// Unreal Engine
#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"

// Generated
#include "GKMLGameModeBase.generated.h"

/**
 *
 */
UCLASS(Blueprintable, BlueprintType)
class GKML_API AGKMLGameModeBase : public AGameModeBase
{
	GENERATED_BODY()

public:
	AGKMLGameModeBase();

	virtual void ResetLevel() override;

	/** Returns true if GameOver() has been called, false otherwise */
	virtual bool HasMatchEnded() const override;

	/** Called when the game is over
	 * i.e. the player dies, the time runs out or the game is finished*/
	UFUNCTION(BlueprintCallable, Category = Game)
	virtual void GameOver();

protected:
	//! Expose ResetLevel to blueprint so we can implement custom logic when the ML environment is reset
	UFUNCTION(BlueprintImplementableEvent, Category = Game, meta = (DisplayName = "ResetLevel", ScriptName = "ResetLevel"))
	void K2_ResetLevel();

	//! Expose GameOver to blueprint so we can cleanup the level before calling ResetLevel
	UFUNCTION(BlueprintImplementableEvent, Category = Game, meta = (DisplayName = "OnGameOver", ScriptName = "OnGameOver"))
	void K2_OnGameOver();

	UPROPERTY(BlueprintReadOnly, Category = Game)
	uint32 bGameOver : 1;
};
