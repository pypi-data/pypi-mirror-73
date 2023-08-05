import autogalaxy as ag
import numpy as np


class TestMaskedImaging:
    def test__masked_dataset_via_autoarray(self, imaging_7x7, sub_mask_7x7):

        masked_imaging_7x7 = ag.MaskedImaging(imaging=imaging_7x7, mask=sub_mask_7x7)

        assert (masked_imaging_7x7.image.in_1d == np.ones(9)).all()

        assert (
            masked_imaging_7x7.image.in_2d == np.ones((7, 7)) * np.invert(sub_mask_7x7)
        ).all()

        assert (masked_imaging_7x7.noise_map.in_1d == 2.0 * np.ones(9)).all()
        assert (
            masked_imaging_7x7.noise_map.in_2d
            == 2.0 * np.ones((7, 7)) * np.invert(sub_mask_7x7)
        ).all()

        assert (masked_imaging_7x7.psf.in_1d == (1.0 / 9.0) * np.ones(9)).all()
        assert (masked_imaging_7x7.psf.in_2d == (1.0 / 9.0) * np.ones((3, 3))).all()
        assert masked_imaging_7x7.psf_shape_2d == (3, 3)

        assert type(masked_imaging_7x7.convolver) == ag.Convolver

    def test__inheritance_from_autoarray(
        self, imaging_7x7, sub_mask_7x7, blurring_grid_7x7
    ):

        masked_imaging_7x7 = ag.MaskedImaging(
            imaging=imaging_7x7,
            mask=sub_mask_7x7,
            grid_class=ag.Grid,
            psf_shape_2d=(3, 3),
            inversion_pixel_limit=20.0,
        )

        assert masked_imaging_7x7.inversion_pixel_limit == 20.0

        grid = ag.Grid.from_mask(mask=sub_mask_7x7)

        assert (masked_imaging_7x7.grid == grid).all()

        blurring_grid = grid.blurring_grid_from_kernel_shape(kernel_shape_2d=(3, 3))

        assert (masked_imaging_7x7.blurring_grid.in_1d == blurring_grid_7x7).all()
        assert (masked_imaging_7x7.blurring_grid == blurring_grid).all()

    def test__modified_image_and_noise_map(
        self, image_7x7, noise_map_7x7, imaging_7x7, sub_mask_7x7
    ):

        masked_imaging_7x7 = ag.MaskedImaging(imaging=imaging_7x7, mask=sub_mask_7x7)

        image_7x7[0] = 10.0
        noise_map_7x7[0] = 11.0

        masked_imaging_7x7 = masked_imaging_7x7.modify_image_and_noise_map(
            image=image_7x7, noise_map=noise_map_7x7
        )

        assert masked_imaging_7x7.image.in_1d[0] == 10.0
        assert masked_imaging_7x7.image.in_2d[0, 0] == 10.0
        assert masked_imaging_7x7.noise_map.in_1d[0] == 11.0
        assert masked_imaging_7x7.noise_map.in_2d[0, 0] == 11.0


class TestSimulatorImaging:
    def test__from_plane_and_grid__same_as_plane_image(self):

        psf = ag.Kernel.from_gaussian(shape_2d=(7, 7), sigma=0.5, pixel_scales=1.0)

        grid = ag.Grid.uniform(shape_2d=(20, 20), pixel_scales=0.05, sub_size=1)

        galaxy_0 = ag.Galaxy(redshift=0.5, light=ag.lp.EllipticalSersic(intensity=1.0))

        galaxy_1 = ag.Galaxy(redshift=1.0, light=ag.lp.EllipticalSersic(intensity=0.3))

        plane = ag.Plane(redshift=0.75, galaxies=[galaxy_0, galaxy_1])

        simulator = ag.SimulatorImaging(
            psf=psf,
            exposure_time_map=ag.Array.full(fill_value=10000.0, shape_2d=grid.shape_2d),
            background_sky_map=ag.Array.full(fill_value=100.0, shape_2d=grid.shape_2d),
            add_noise=True,
            noise_seed=1,
        )

        imaging = simulator.from_plane_and_grid(plane=plane, grid=grid)

        assert (imaging.image.in_2d == imaging.image.in_2d).all()
        assert (imaging.psf == imaging.psf).all()
        assert (imaging.noise_map == imaging.noise_map).all()

    def test__simulate_imaging_from_galaxy__source_galaxy__compare_to_imaging(self):

        galaxy_0 = ag.Galaxy(
            redshift=0.5,
            mass=ag.mp.EllipticalIsothermal(
                centre=(0.0, 0.0), einstein_radius=1.6, elliptical_comps=(0.17647, 0.0)
            ),
        )

        galaxy_1 = ag.Galaxy(
            redshift=1.0,
            light=ag.lp.EllipticalSersic(
                centre=(0.1, 0.1),
                elliptical_comps=(0.096225, -0.055555),
                intensity=0.3,
                effective_radius=1.0,
                sersic_index=2.5,
            ),
        )

        grid = ag.Grid.uniform(shape_2d=(11, 11), pixel_scales=0.2, sub_size=1)

        psf = ag.Kernel.no_blur(pixel_scales=0.2)

        simulator = ag.SimulatorImaging(
            psf=psf,
            exposure_time_map=ag.Array.full(fill_value=10000.0, shape_2d=grid.shape_2d),
            background_sky_map=ag.Array.full(fill_value=100.0, shape_2d=grid.shape_2d),
            add_noise=True,
            noise_seed=1,
        )

        imaging = simulator.from_galaxies_and_grid(
            galaxies=[galaxy_0, galaxy_1], grid=grid
        )

        plane = ag.Plane(redshift=0.75, galaxies=[galaxy_0, galaxy_1])

        imaging_via_image = simulator.from_image(image=plane.image_from_grid(grid=grid))

        assert (imaging.image == imaging_via_image.image).all()
        assert (imaging.psf == imaging_via_image.psf).all()
        assert imaging.noise_map == imaging_via_image.noise_map
