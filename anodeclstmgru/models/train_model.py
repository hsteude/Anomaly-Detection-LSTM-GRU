from anodeclstmgru.models.lit_module import AutoEncoderLitModule 
import pytorch_lightning as pl
import argparse
from pytorch_lightning import seed_everything
from anodeclstmgru.data.data_module import SWaTSDataModule

seed_everything(42)


def main(args):
    # debugging forward pass
    lit_module = AutoEncoderLitModule(**vars(args))
    trainer = pl.Trainer.from_argparse_args(args)
    data_module = SWaTSDataModule()
    trainer.fit(lit_module, data_module)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # trainer related args
    parser = pl.Trainer.add_argparse_args(parser)

    # encoder related args
    # parser.add_argument('--enc_dr_rate', type=float, default=0)
    # parser.add_argument('--enc_rnn_hidden_dim', type=int, default=6)
    # parser.add_argumnt('--enc_rnn_num_layers', type=int, default=1)
    # parser.add_argument('--enc_num_hidden_states', type=int, default=1)
    # parser.add_argument('--enc_pretrained', default=True,
                        # action=argparse.BooleanOptionalAction)
    # parser.add_argument('--enc_fixed_cnn_weights', default=True,
                        # action=argparse.BooleanOptionalAction)

    # # lit_module related args
    # parser.add_argument('--learning_rate', type=float, default=0.001)
    # parser.add_argument('--batch_size', type=int, default=12)
    # parser.add_argument('--dl_num_workers', type=int, default=12)
    # parser.add_argument('--validdation_split', type=float, default=0.05)

    args = parser.parse_args()
    main(args)
