// BSD 3-Clause License Copyright (c) 2022, Pierre Delaunay All rights reserved.


#include "GKMLPawn.h"

// Sets default values
AGKMLPawn::AGKMLPawn()
{
 	// Set this pawn to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;

}

// Called when the game starts or when spawned
void AGKMLPawn::BeginPlay()
{
	Super::BeginPlay();

}

// Called every frame
void AGKMLPawn::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

}

// Called to bind functionality to input
void AGKMLPawn::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);

}

