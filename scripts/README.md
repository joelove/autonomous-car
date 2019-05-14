## AWS instances

> **Lima**
>
> ubuntu@13.59.126.84

> **Sierra**
>
> ubuntu@13.58.255.178

> **Charlie**
>
> ubuntu@3.17.143.7


## Running the training script

1. Connect to the AWS instance

```bash
ssh ubuntu@1.1.1.1
```

2. Navigate to the project directory

```bash
cd projects/autonomous-car
```

3. Confirm we have training data available

```bash
ls -l data/
```

4. Run the script

```bash
python scripts/train_model.py --help
```

5. View the training information on TensorBoard

> https://1.1.1.1:6006


## Setting up an AWS instance

1. Connect to the AWS instance

```bash
ssh ubuntu@1.1.1.1
```

2. Create a projects directory

```bash
mkdir projects
cd projects
```

3. Clone the repo

```bash
git clone https://github.com/joelove/autonomous-car.git
```

4. Install dependencies for scripts

```bash
pip install --upgrade pip
pip uninstall sagemaker
pip install opencv-python tensorflow-gpu==1.12.0 tensorboard==1.12.2 pillow
```

## Raspberry Pi commands

Upload **from** Raspberry pi to AWS instances

```bash
rsync -azr -v --stats --progress ./data/* ubuntu@13.59.126.84:~/projects/autonomous-car/data
rsync -azr -v --stats --progress ./data/* ubuntu@13.58.255.178:~/projects/autonomous-car/data
rsync -azr -v --stats --progress ./data/* ubuntu@3.17.143.7:~/projects/autonomous-car/data
```

Download data **to** local machine from Raspberry Pi

```bash
rsync -azr -v --stats --progress pi@10.134.152.241:~/Projects/autonomous-car/data/* ./data
```

Download a model **to** the Raspberry Pi from an AWS instance

```bash
rsync -azr -v --stats --progress ubuntu@13.59.126.84:~/projects/autonomous-car/model.json ./
rsync -azr -v --stats --progress ubuntu@13.59.126.84:~/projects/autonomous-car/model.h5 ./
```
