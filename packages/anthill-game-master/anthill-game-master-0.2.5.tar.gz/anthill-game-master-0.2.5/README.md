# Game Service

When it comes to hosting a server for a multiplayer game, major problems appear:

1. Game servers actually need to be put somewhere;
2. The life cycle of the game server need to be maintained (as game servers may crash or become outdated);
3. The players should be "matchmaked" either by region (to ensure low latency) or by custom set or/and rules
(completely game-specific, for example, a user level, map, or game mode);
4. The system overall must be scalable to add new servers into the pool when the concurrent players number explode;
5. Binary files of the game server need to be deployed to all host machines (the more machines are, harder it is).

This service solves them all, the rest is completely up to the game.

<b>Note</b>: Game Service covers one part of the matchmaking services only.
See <a href="https://github.com/anthill-platform/anthill-game-controller#game-controller">Controller Service</a> for
another part.

## API

Please refer to the <a href="doc/API.md">API Documentation</a> for more information.

## Concepts

Game Service is actually made out of two services: a Master Service and a Controller Service. 

* **Master Service**. Master Service is a part of Game Service that holds the information about
all rooms and balances Players across multiple Hosts. Also it heartbeats health status of each Host and routes
Players to a healthy one if some Host dies.

* **Controller Service**. Controller Service is a second part of Game Service. It runs on a 
certain Host and spawns Game Server instance on it when requested by Master Service. Also it heartbeats health status 
of each Game Server running on Host and stops it if it stops responding or crashes. 
<a href="https://github.com/anthill-platform/anthill-game-controller#game-controller">See Controller Service documentation.</a>

* **Room**. Room represents a single game instance the player may join. Each room has a limit
of maximum players on it and may contain custom setting to search upon.

* **Game Server**. Game Server (GS) is a completely game-specific piece of software that runs server side, holds a
single game instance and a may be addressed by according room.

* **Host**. Host is actually a single hardware machine that can run multiple Game Servers on itself.
Since only limited number of Game Servers can be spawned on each host due to hardware limitations, multiple hosts
may be grouped by a Region.

* **Region**. Region is a group of Hosts (even with a single one) that physically located on a same geographical region
(or Data Center). Players may search rooms only on certain Region to ensure low latency.

* **Party**. In certain cases, partying players together is required before (or without) the actual Game Server being instantiated:
  
  * You want to start the Game Server only when full room of people is matched;
  * Players want to discuss the future map / game mode before starting the game;
  * Players want to join a random game with their friends.
  
  Please see <a href="doc/Party.md">Party Documentation</a> for more information.

## Overall Architecture

<center>
<img src="https://cloud.githubusercontent.com/assets/1666014/26266946/613bc5a0-3cf0-11e7-9c1e-59e403ea5bdd.png" width="954">
</center>