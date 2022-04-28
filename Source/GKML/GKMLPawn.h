// BSD 3-Clause License Copyright (c) 2022, Pierre Delaunay All rights reserved.

#pragma once

// Unreal Engine
#include "CoreMinimal.h"
#include "GameFramework/Pawn.h"
#include "GenericTeamAgentInterface.h"

// Generated
#include "GKMLPawn.generated.h"

UCLASS(Blueprintable, BlueprintType)
class GKML_API AGKMLPawn : public APawn, public IGenericTeamAgentInterface
{
	GENERATED_BODY()

public:
	// Sets default values for this pawn's properties
	AGKMLPawn();

protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

	virtual FGenericTeamId GetGenericTeamId() const { return FGenericTeamId(TeamId); }

	//! Make our base pawn hostile to everything.
	//! this will make AIPerception/AISense_Sight gets triggered for every actors
	virtual ETeamAttitude::Type GetTeamAttitudeTowards(const AActor& Other) const override
	{
		return ETeamAttitude::Hostile;
	}

public:
	//! Expose the TeamdId to blueprint
	UPROPERTY(EditAnywhere, Category = Team)
	uint8 TeamId;

	// Called every frame
	virtual void Tick(float DeltaTime) override;

	// Called to bind functionality to input
	virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

};
