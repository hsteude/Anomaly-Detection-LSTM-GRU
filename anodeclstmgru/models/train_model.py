from anodeclstmgru.models.lit_module import AutoEncoderLitModule
import pytorch_lightning as pl
import argparse
from pytorch_lightning import seed_everything
from anodeclstmgru.data.data_module import SWaTSDataModule

seed_everything(42)


def main(args):
    # debugging forward pass
    data_module = SWaTSDataModule(**vars(args))
    vars(args).update(dict(
        input_size=data_module.size()[2],
        seq_len=data_module.size()[1]))
    lit_module = AutoEncoderLitModule(**vars(args))
    trainer = pl.Trainer.from_argparse_args(args)
    trainer.fit(lit_module, data_module)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # trainer related args
    parser = pl.Trainer.add_argparse_args(parser)

    # data module related
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--window_size', type=int, default=100)
    parser.add_argument('--sample_size', type=int, default=1000)
    parser.add_argument('--sample_freq', type=str, default='5s')
    parser.add_argument('--validation_split', type=float, default=0.05)
    parser.add_argument('--num_workers', type=int, default=12)
    # Lit Module related
    parser = AutoEncoderLitModule.add_model_specific_args(parser)
    args = parser.parse_args()
    main(args)
