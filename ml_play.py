from games.arkanoid.communication import (
    SceneInfo, GameStatus, PlatformAction
)
import games.arkanoid.communication as comm
"""
The template of the main script of the machine learning process
"""
ball_x = []
ball_y = []
final = 0


def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False

    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()
    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()

        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
                scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information

        ball_x.append(scene_info.ball[0])
        ball_y.append(scene_info.ball[1])
        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_instruction(
                scene_info.frame, PlatformAction.SERVE_TO_RIGHT)
            ball_served = True
        else:
            global final
            if(scene_info.ball[1] > 200):
                if (scene_info.ball[1] - ball_y[-2] > 0):      # 球往下
                    if (scene_info.ball[0] - ball_x[-2] > 0):  # 球往右
                        final = (400-scene_info.ball[1])+scene_info.ball[0]
                        if (final > 200):
                            final = 400 - final
                    else:  # 往左
                        final = scene_info.ball[0]-(400 - scene_info.ball[1])
                        if (final < 0):
                            final = -final
                if (scene_info.platform[0]+10 > final):
                    comm.send_instruction(
                        scene_info.frame, PlatformAction.MOVE_LEFT)
                elif (scene_info.platform[0]+10 < final):
                    comm.send_instruction(
                        scene_info.frame, PlatformAction.MOVE_RIGHT)
            else:
                if (scene_info.platform[0]+10 > scene_info.ball[0]):
                    comm.send_instruction(
                        scene_info.frame, PlatformAction.MOVE_LEFT)
                else:
                    comm.send_instruction(
                        scene_info.frame, PlatformAction.MOVE_RIGHT)
