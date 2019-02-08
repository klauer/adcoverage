import ophyd
import ophyd.sim
import ophyd.areadetector.common_plugins as plugins

for cls, pvfn in [
        (plugins.CommonPlugins_V20, 'R2-0'),
        (plugins.CommonPlugins_V21, 'R2-1'),
        (plugins.CommonPlugins_V22, 'R2-2'),
        (plugins.CommonPlugins_V23, 'R2-3'),
        (plugins.CommonPlugins_V24, 'R2-4'),
        (plugins.CommonPlugins_V25, 'R2-5'),
        (plugins.CommonPlugins_V26, 'R2-6'),
        (plugins.CommonPlugins_V31, 'R3-1'),
        (plugins.CommonPlugins_V32, 'R3-2'),
        (plugins.CommonPlugins_V33, 'R3-3'),
        (plugins.CommonPlugins_V34, 'R3-4'),
        ]:

    print('')
    print('')
    print('----------------------------------------------------------------')
    print(cls.__name__)
    for attr, subdev in cls.walk_subdevice_classes():
        subdev.lazy_wait_for_connection = False

    plugin = cls(prefix='PREFIX:', name='test')

    pvs = [walk.item.pvname for walk in plugin.walk_signals(include_lazy=True)
           if hasattr(walk.item, 'pvname')
           ]
    pvs.extend([walk.item.setpoint_pvname
                for walk in plugin.walk_signals(include_lazy=True)
                if hasattr(walk.item, 'setpoint_pvname')
                ])

    pvs = set(pvs)

    with open(f'pvlists/{pvfn}.txt', 'rt') as f:
        from_ioc = [pv.strip() for pv in f.readlines()]

    print(pvfn, 'total pvs in ophyd', len(pvs), 'of', len(from_ioc),
          ': PVs from IOC', (float(len(pvs)) / len(from_ioc)) * 100.0, '%')

    missing = set(from_ioc) - pvs

    if missing:
        for pv in sorted(missing):
            print('*', 'MISSING', pv, pvfn)

        print()
        print()
        print()

    errors = set(pvs) - set(from_ioc)
    if errors:
        print('Should not exist!')
        for pv in sorted(errors):
            print('*', 'ERROR', pv, pvfn)
