// BSD 3-Clause License Copyright (c) 2022, Pierre Delaunay All rights reserved.


#include "GKMLGameModeBase.h"


AGKMLGameModeBase::AGKMLGameModeBase() {
	bGameOver = false;
}

void AGKMLGameModeBase::ResetLevel()
{
	K2_ResetLevel();
}

bool AGKMLGameModeBase::HasMatchEnded() const
{
	return bGameOver;
}

void AGKMLGameModeBase::GameOver()
{
	if (bGameOver == false)
	{
		K2_OnGameOver();
		bGameOver = true;
	}
}
