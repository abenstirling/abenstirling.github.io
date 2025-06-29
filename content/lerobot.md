+++
title = 'LeRobot'
date = 2025-06-15
draft = false

[extra]
[extra.cover]
    image = "/images/lerobot_cover.webp"
    relative = true
+++

I took a break from robotics after a machine learning project on [semantic naviation](https://github.com/abenstirling/SemanticNavigation). 


I was at a christmas party and heard about an open-source initiative for 6 [DoF](https://en.wikipedia.org/wiki/Degrees_of_freedom_(mechanics)). There were even Bambu files, so I printed the SO-100 and got to assembling it as soon as my motors arrived. 
![LeRobot Implementation](/posts/lerobot_1.webp)

There was an issue where the motor (specifically just the 3rd joint from the bottom) would just be blinking and not work at all. I tried getting help, but I gave up and packed it away for a bit. 

After a 3 month break and moving to a different apartment, I pulled it out and debugged the motor and finally got it working

![LeRobot teleop](/posts/lerobot_3.webp)

The above ran with the following command: 
```
python lerobot/scripts/control_robot.py \
  --robot.type=so100 \
  --control.type=teleoperate
```
This is teleoperation "teleop" where I have the leader arm and the follower arm. 

## Goals
Let us define goals for this project:
- train robot to do a custom task 
- have it do it autonomously with a 80%+ success rate

![LeRobot working](/posts/lerobot_2.webp)

**Move-T** is my challenge. The goal is to place the red T on the yellow outline. 

### 1st Attempt
- macbook (weird front scene camera)
- iphone continuity (overhead camera)
- 40 tests
    - 10 repeats per initial spot

I ran the following command to get data: 
```
python lerobot/scripts/control_robot.py \
  --robot.type=so100 \
  --control.type=record \
  --control.fps=30 \
  --control.single_task="Move T to where it belongs." \
  --control.repo_id=${HF_USER}/so100_move_t2 \
  --control.tags='["so100","tutorial"]' \
  --control.warmup_time_s=10 \
  --control.episode_time_s=15 \
  --control.reset_time_s=15 \
  --control.num_episodes=40 \
  --control.push_to_hub=true
```
Note: I pushed to hugging face in case my macbook dies during training. 

**Results**: 
![Results 1](/posts/lerobot_4.webp)
This took **26 HOURS** to train. This was eye-opening. It was garbage 

Learnings: 
- need to find a way to train faster to shorten feedback loop
- need to debug data with wandb (weights and biases)
- review the data (literally comb through it to make sure that cameras aren't off or something)

### 2nd Attempt

I began to think about the problem from first principles. 

I was moving around from the laptop's perspective, and I believed that 

So I deleted my laptop footage from hugging face by simply deleting the folder via their website. 

![Deleting data](/posts/lerobot_5.webp)

I also found that you could [train your model by renting an A100](https://huggingface.co/docs/lerobot/notebooks). This would help solve the long feedback loop issue. 

The workflow was: 
```
colab -> setup lerobot -> download training data (hf) -> train -> upload model (hf)
```

**Results**

This took **2h 14m 52s** to train. The cost was $2.33. 

![Attempt 2](/posts/lerobot_6.webp)

Here is the wandb results: 
![Attempt 2 wandb](/posts/lerobot_7.webp)

Ok so the task was not completed, but we learned the following: 
- data is the large driver in the output of the arm 
- colab is necessary for speed 

## 3rd Attempt
I began researching what other successful systems did. 

![Aloha setup](/posts/lerobot_8.webp)

and based on this meme of a statement:

![meme](/posts/lerobot_9.webp)

I added a wrist camera, and moved the overhead camera to be a side camera. 

![wrist camera](/posts/lerobot_10.webp)

![setup](/images/lerobot_cover.webp)




---
Still in progress: 

Q: My brother asked a good question, why do we have to have a leader and follower arm? Why can't you just guide a single arm? 

A: My response was that we are using a VLA, so having the human moving is throwing off the visual encoding. 