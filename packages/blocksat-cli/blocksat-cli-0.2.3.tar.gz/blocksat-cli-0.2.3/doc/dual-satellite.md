# Dual-Satellite Connection

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->
**Table of Contents**

- [Dual-Satellite Connection](#dual-satellite-connection)
    - [Novra S400 standalone demodulator](#novra-s400-standalone-demodulator)
    - [TBS5927 USB demodulator](#tbs5927-usb-demodulator)
    - [SDR-based demodulator](#sdr-based-demodulator)

<!-- markdown-toc end -->


Some regions worldwide are covered by two satellites at the same time. For
example, most of the US has coverage from both the Galaxy 18 and Eutelsat 113
satellites. In Asian, there is extensive overlapping coverage from Telstar 18V C
and Telstar 18V Ku.

You can check if your location has overlapping coverage from two satellites by
checking our [Coverage
Map](https://blockstream.com/satellite/#satellite_network-coverage).

If you are located in such a region, you can connect to the two satellites
simultaneously and double the speed of bitcoin block transfers.

To do so, you need two full (independent) receiver setups, with separate
antennas, each pointed to a different satellite. You then need to run the
receivers normally (independently) and configure bitcoin-satellite to get data
from both of them. If you have the Novra S400 receiver of the [Pro Ethernet
Kit](https://store.blockstream.com/product/blockstream-satellite-pro-kit/). (w/
Standalone Demodulator), you only need this single receiver unit, which can be
connected to the two antennas/LNBs.

To run multiple receivers, you can use separate configurations on the CLI. For
example, your first step with the CLI regardless of the type of receiver is to
run the configuration helper, as follows:

```
blocksat-cli cfg
```

To configure a second receiver, you can add option `--cfg name`, where `name` is
the name of the second configuration. For example, set up a configuration named
`rx2` as follows:

```
blocksat-cli --cfg rx2 cfg
```

Then, you can run all commands in the CLI with option `--cfg rx2`. Specific
instructions are provided next.


## Novra S400 standalone demodulator

## TBS5927 USB demodulator




For example, with a USB demodulator, you would normally run the
following sequence of commands:

1. Initial configurations:
```
blocksat-cli cfg
```

2. Installation of dependencies:
```
blocksat-cli deps install
```

3. Configuration of the host interfaces:
```
sudo blocksat-cli usb config
```

4. Receiver launch:
```
blocksat-cli usb launch
```

If you wanted to communicate to a second receiver (regardless of being USB,
standalone, or SDR), you can switch configurations using argument `--cfg` of the
CLI. For example, suppose your have another USB demodulator. You could then
create another configuration named, for instance, `rx2`, as follows:

```
blocksat-cli --cfg rx2 cfg
```

Then, you can run the same commands as before, but adding option `--cfg rx2` on
them, as follows:

```
blocksat-cli --cfg rx2 deps install

sudo blocksat-cli --cfg rx2 usb config

blocksat-cli --cfg rx2 usb launch
```


## SDR-based demodulator
