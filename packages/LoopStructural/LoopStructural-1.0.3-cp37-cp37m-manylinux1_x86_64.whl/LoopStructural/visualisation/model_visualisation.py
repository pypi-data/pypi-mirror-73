"""
A wrapper for lavavu

"""

import logging

import lavavu
import numpy as np
from lavavu.vutils import is_notebook
from skimage.measure import marching_cubes_lewiner as marching_cubes

from LoopStructural.utils.helper import create_surface, get_vectors, create_box

logger = logging.getLogger(__name__)
# adapted/copied from pyvista for sphinx scraper
_OPEN_VIEWERS = {}

def close_all():
    _OPEN_VIEWERS.clear()
    return True
    # for key, v in _OPEN_VIEWERS.items():
    #     if not v._closed:
    #         v.close()
    #     v.deep_clean()
    # _OPEN_VIEWERS.clear()
    # return True
##
class LavaVuModelViewer:
    """

    Short description

    """
    def __init__(self, model=None, bounding_box=None, nsteps=None, vertical_exaggeration=1., **kwargs):
        """
        A wrapper to plot LoopStructural object with lavavu

        Parameters
        ----------
        **kwargs : lavavu viewer kwargs

        Attributes
        ----------
        lv Lavavu.Viewer object
        objects : dictionary of objects that have been plotted
        """
        # copied from pyvista
        self._id_name = "{}-{}".format(str(hex(id(self))), len(_OPEN_VIEWERS))
        _OPEN_VIEWERS[self._id_name] = self
        #
        self.lv = lavavu.Viewer(**kwargs)
        self.lv['orthographic'] = True
        self.lv.modelscale([1,1,vertical_exaggeration])
        self.objects = {}
        self.bounding_box = bounding_box
        self.nsteps = nsteps
        if model is not None:
            self.bounding_box = model.bounding_box
            self.nsteps = model.nsteps
            logger.debug("Using bounding box from model")
        if self.bounding_box is None or self.nsteps is None:
            logger.error("Plot area has not been defined.")
        self.bounding_box = np.array(self.bounding_box)
        self.nsteps = np.array(self.nsteps)
        self.model = model
        # prerotate to a nice view
        # self.lv.rotate([-57.657936096191406, -13.939384460449219, -6.758780479431152])
    def close(self):
        pass

    def deep_clean(self):
        """[summary]

        [extended_summary]
        """
        self.lv.clear()
        self.lv.cleardata()
        pass

    def add_section(self, geological_feature=None, axis='x', value=None, **kwargs):
        """

        Plot a section/map thru the model and paint with a geological feature

        Parameters
        ----------
        geological_feature : Geological feature
            The feature to paint the section with
        axis : string
            which axis, x,y,z
        value : float
            Where to make the section
        kwargs
            additional kwargs passes to lavavu for colourmaps etc

        Returns
        -------

        """

        if axis == 'x':
            tri, yy, zz = create_surface(self.bounding_box[:, [1, 2]], self.nsteps[[1, 2]])
            xx = np.zeros(zz.shape)
            if value is None:
                xx[:] = np.nanmean(self.bounding_box[:, 0])
            else:
                xx[:] = value
        if axis == 'y':
            tri, xx, zz = create_surface(self.bounding_box[:, [0, 2]], self.nsteps[[0, 2]])
            yy = np.zeros(xx.shape)
            if value is None:
                yy[:] = np.nanmean(self.bounding_box[:, 1])
            else:
                yy[:] = value
        if axis == 'z':
            tri, xx, yy = create_surface(self.bounding_box[:, 0:2], self.nsteps[0:2])
            zz = np.zeros(xx.shape)
            if value is None:
                zz[:] = np.nanmean(self.bounding_box[:, 2])
            else:
                zz[:] = value
        name = kwargs.get('name', axis + '_slice')
        colour = kwargs.get('colour', 'red')

        # create an array to evaluate the feature on for the section
        points = np.zeros((len(xx), 3))  #
        points[:, 0] = xx
        points[:, 1] = yy
        points[:, 2] = zz

        surf = self.lv.triangles(name)
        surf.vertices(points)
        surf.indices(tri)
        logger.info("Adding %s section at %f" % (axis, value))
        if geological_feature is None:
            surf.colours(colour)
        if geological_feature is not None:
            if 'norm' in kwargs:
                surf.values(np.linalg.norm(
                    geological_feature.evaluate_gradient(points), axis=1),
                    geological_feature.name)
            else:
                surf.values(geological_feature.evaluate_value(points),
                            geological_feature.name)
            surf["colourby"] = geological_feature.name
            cmap = lavavu.cubehelix(100)
            if 'cmap' in kwargs:
                cmap = kwargs['cmap']
            logger.info("Colouring section with %s min: %f, max: %f" % (
                geological_feature.name, geological_feature.min(), geological_feature.max()))
            surf.colourmap(cmap, range=[geological_feature.min(), geological_feature.max()])

    def add_isosurface(self, geological_feature, value = None, isovalue=None,
                     paint_with=None, slices=None, colour='red', nslices=None, 
                     cmap=None, filename=None, **kwargs):
        """ Plot the surface of a geological feature 

        [extended_summary]

        Parameters
        ----------
        geological_feature : GeologicalFeature
            [description]
        value : float, optional

        isovalue : [type], optional
            [description], by default None
        paint_with : [type], optional
            [description], by default None
        slices : [type], optional
            [description], by default None
        colour : [type], optional
            [description], by default None
        nslices : [type], optional
            [description], by default None
        cmap : [type], optional
            [description], by default None
        filename: string, optional
            filename for exporting 

        Returns
        -------
        [type]
            [description]
        """

        # update the feature to make sure its current
        if 'update' in kwargs:
            geological_feature.update()


        # do isosurfacing of support using marching tetras/cubes
        x = np.linspace(self.bounding_box[0, 0], self.bounding_box[1, 0], self.nsteps[0])
        y = np.linspace(self.bounding_box[0, 1], self.bounding_box[1, 1], self.nsteps[1])
        z = np.linspace(self.bounding_box[1, 2], self.bounding_box[0, 2], self.nsteps[2])
        xx, yy, zz = np.meshgrid(x, y, z, indexing='ij')
        points = np.array([xx.flatten(), yy.flatten(), zz.flatten()]).T
        val = geological_feature.evaluate_value(points)
        # get the stats to check what we are plotting
        mean_property_val = np.nanmean(val)#geological_feature.mean()
        min_property_val = np.nanmin(val)#geological_feature.min()
        max_property_val = np.nanmax(val)#geological_feature.max()
        # set default parameters
        slices_ = [mean_property_val]
        painter = None
        voxet = None
        tris = None
        nodes = None
        # parse kwargs for parameters
        if isovalue is not None:
            slices_ = [isovalue]
        if value is not None:
            slices_ = [value]
        if slices is not None:
            slices_ = slices
        if nslices is not None:
            var = max_property_val - min_property_val
            # buffer slices by 5%
            slices_ = np.linspace(min_property_val + var * 0.05,
                                 max_property_val - var * 0.05,
                                 nslices)

        if paint_with is not None:
            painter = paint_with

        region = kwargs.get('region', None)


        if region is not None:
            val[~region(np.array([xx.flatten(), yy.flatten(), zz.flatten()]).T)] = np.nan
        step_vector = np.array([x[1] - x[0], y[1] - y[0], z[1] - z[0]])
        for isovalue in slices_:
            logger.info("Creating isosurface of %s at %f" % (geological_feature.name, isovalue))

            if isovalue > np.nanmax(val) or isovalue < np.nanmin(val):
                logger.warning("Isovalue doesn't exist inside bounding box")
                continue  # return np.zeros((3, 1)).astype(int), np.zeros((3, 1))
            try:
                verts, faces, normals, values = marching_cubes(
                    val.reshape(self.nsteps, order='C'),
                    isovalue,
                    spacing=step_vector)
                verts += np.array([self.bounding_box[0, 0], self.bounding_box[0, 1], self.bounding_box[1, 2]])
            except ValueError:
                logger.warning("no surface to mesh, skipping")
                continue
            

            name = geological_feature.name
            name = kwargs.get('name', name)
            name += '_iso_%f' % isovalue
            if filename is not None:
                try:
                    import meshio
                except ImportError:
                    logger.error("Could not save surfaces, meshio is not installed")
                meshio.write_points_cells(filename.format(name),
                self.model.rescale(verts),
                [("triangle", faces)]
                )
            surf = self.lv.triangles(name)
            surf.vertices(verts)
            surf.indices(faces)
            if painter is None:
                surf.colours(colour)
            if painter is not None:
                # add a property to the surface nodes for visualisation
                # calculate the mode value, just to get the most common value
                surfaceval = np.zeros(verts.shape[0])
                surfaceval[:] = painter.evaluate_value(verts)
                if painter.name is geological_feature.name:
                    logger.info("Setting surface value to %f"%isovalue)
                    surfaceval[:] = isovalue
                surf.values(surfaceval, painter.name)
                surf["colourby"] = painter.name               
                vmin = kwargs.get('vmin', min_property_val)
                vmax = kwargs.get('vmax', max_property_val)
                surf.colourmap(cmap, range=(vmin, vmax))  # nodes.shape[0]))
        
    def add_scalar_field(self, geological_feature, **kwargs):
        """

        Parameters
        ----------
        geological_feature : GeologicalFeature
            the geological feature to colour the scalar field by
        kwargs
            kwargs for lavavu

        Returns
        -------

        """
        name = kwargs.get('name', geological_feature.name + '_scalar_field')
        points, tri = create_box(self.bounding_box,self.nsteps)

        surf = self.lv.triangles(name)
        surf.vertices(points)
        surf.indices(tri)
        val =geological_feature.evaluate_value(points)
        surf.values(val, geological_feature.name)
        surf["colourby"] = geological_feature.name
        cmap = kwargs.get('cmap',lavavu.cubehelix(100))

        logger.info("Adding scalar field of %s to viewer. Min: %f, max: %f" % (geological_feature.name,
                                                                               geological_feature.min(),
                                                                               geological_feature.max()))
        vmin = kwargs.get('vmin', np.nanmin(val))
        vmax = kwargs.get('vmax', np.nanmax(val))
        surf.colourmap(cmap, range=(vmin, vmax))

    def add_model(self, **kwargs):
        """Add a block model painted by stratigraphic id to the viewer

        Calls self.model.evaluate_model() for a cube surrounding the model.

        Notes
        ------
        It is sensible to increase the viewer step sizes before running this function to
        increase the resolution of the model as its not possible to interpolate a discrete
        colourmap and this causes the model to look like a lego block.
        You can update the model resolution by changing the attribute nsteps
        >>> viewer.nsteps = np.array([100,100,100])

        """
        name = kwargs.get('name', 'geological_model')
        points, tri = create_box(self.bounding_box, self.nsteps)

        surf = self.lv.triangles(name)
        surf.vertices(points)
        surf.indices(tri)
        val = self.model.evaluate_model(points,rescale=False)
        surf.values(val, 'model')
        surf["colourby"] = 'model'
        cmap = kwargs.get('cmap', lavavu.cubehelix(100))

        # logger.info("Adding scalar field of %s to viewer. Min: %f, max: %f" % (geological_feature.name,
        #                                                                        geological_feature.min(),
        #                                                                        geological_feature.max()))
        vmin = kwargs.get('vmin', np.nanmin(val))
        vmax = kwargs.get('vmax', np.nanmax(val))
        surf.colourmap(cmap, range=(vmin, vmax))

    def add_model_surfaces(self, faults = True, cmap='tab20', **kwargs):
        """Add surfaces for all of the interfaces in the model


        Parameters
        ----------
        faults : bool, optional
            whether to draw faults, by default True
        cmap : string
            matplotlib cmap
        Notes
        ------
        Other parameters are passed to self.add_isosurface() 

        """
        from matplotlib import cm
        n_units = 0 #count how many discrete colours
        for g in self.model.stratigraphic_column.keys():
            for u in self.model.stratigraphic_column[g].keys():
                n_units+=1
        tab = cm.get_cmap(cmap,n_units)
        ci = 0

        for g in self.model.stratigraphic_column.keys():
            if g in self.model.feature_name_index:
                feature = self.model.features[self.model.feature_name_index[g]]
                for u, vals in self.model.stratigraphic_column[g].items():
                    self.add_isosurface(feature, isovalue=vals['max'],name=u,colour=tab.colors[ci,:],**kwargs)
                    ci+=1
        if faults:
            for f in self.model.features:
                if f.type == 'fault':
                    self.add_isosurface(f,isovalue=0,**kwargs)


    def add_vector_field(self, geological_feature, **kwargs):
        """

        Plot the gradient of a geological feature at given locations

        Parameters
        ----------
        geological_feature : Geological Feature to evaluate gradient
        locations : ((N,3)) array of evaluation locations
        kwargs : kwargs for lavavu vector

        Returns
        -------

        """
        logger.info("Adding vector field for %s " % (geological_feature.name))
        locations = kwargs.get('locations', None)
        if locations is None:
            x = np.linspace(self.bounding_box[0, 0], self.bounding_box[1, 0], self.nsteps[0])
            y = np.linspace(self.bounding_box[0, 1], self.bounding_box[1, 1], self.nsteps[1])
            z = np.linspace(self.bounding_box[1, 2], self.bounding_box[0, 2], self.nsteps[2])
            xx, yy, zz = np.meshgrid(x, y, z, indexing='ij')
            locations = np.array([xx.flatten(), yy.flatten(), zz.flatten()]).T
        vector = geological_feature.evaluate_gradient(locations)
        # normalise
        mask = ~np.any(np.isnan(vector), axis=1)
        vector[mask, :] /= np.linalg.norm(vector[mask, :], axis=1)[:, None]
        vectorfield = self.lv.vectors(geological_feature.name + "_grad",
                                      **kwargs)
        vectorfield.vertices(locations[mask, :])
        vectorfield.vectors(vector[mask, :])
        return

    def add_data(self, feature, **kwargs):
        """

        Plot the data linked to the feature, can choose whether to plot all data types
        using value and grad kwargs

        Parameters
        ----------
        feature
        kwargs

        Returns
        -------

        """
        name = feature.name
        add_grad = True
        add_value = True
        add_tang = True
        if 'name' in kwargs:
            name = kwargs['name']
            del kwargs['name']
        if 'grad' in kwargs:
            add_grad = kwargs['grad']
        if 'value' in kwargs:
            add_value = kwargs['value']
        if 'tang' in kwargs:
            add_tang = kwargs['tang']
        grad = feature.builder.get_gradient_constraints()
        norm = feature.builder.get_norm_constraints()
        value = feature.builder.get_value_constraints()
        tang = feature.builder.get_tangent_constraints()
        if grad.shape[0] > 0 and add_grad:
            self.add_vector_data(grad[:, :3], grad[:, 3:6], name + "_grad_cp",
                                 **kwargs)

        if norm.shape[0] > 0 and add_grad:
            self.add_vector_data(norm[:, :3], norm[:, 3:6], name + "_norm_cp",
                                 **kwargs)
        if value.shape[0] > 0 and add_value:
            kwargs['range'] = [feature.min(), feature.max()]
            self.add_value_data(value[:, :3], value[:, 3], name + "_value_cp",
                                **kwargs)
        if tang.shape[0] > 0 and add_tang:
            self.add_vector_data(tang[:, :3], tang[:, 3:6], name + "_tang_cp",
                                 **kwargs)


    def add_points(self, points, name, **kwargs):
        """

        Plot points location in the lavavu viewer

        Parameters
        ----------
        points : numpy array of the points locations
        name :  string name of the object for lavavu
        **kwargs : lavavu points kwargs

        Returns
        -------

        """
        p = self.lv.points(name, **kwargs)
        p.vertices(points)

    def add_vector_data(self, position, vector, name, **kwargs):
        """

        Plot point data with a vector component into the lavavu viewer

        Parameters
        ----------
        position : numpy array N,3 for xyz locations
        vector : numpy array of vector N,3
        name :  string name for the object in lavavu
        kwargs to pass to lavavu

        Returns
        -------

        """
        if 'colour' not in kwargs:
            kwargs['colour'] = 'black'
        # normalise
        if position.shape[0] > 0:
            vector /= np.linalg.norm(vector, axis=1)[:, None]
            vectorfield = self.lv.vectors(name, **kwargs)
            vectorfield.vertices(position)
            vectorfield.vectors(vector)
            return

    def add_value_data(self, position, value, name, **kwargs):
        """

        Plot points data with a value component

        Parameters
        ----------
        position : numpy array N,3 for xyz locations
        value : N array of values
        name :  string name of the object for lavavu
        kwargs : kwargs to pass to lavavu

        Returns
        -------

        """
        if "pointtype" not in kwargs:
            kwargs["pointtype"] = "sphere"
        if "pointsize" not in kwargs:
            kwargs["pointsize"] = 4
        # set the colour map to diverge unless user decides otherwise
        cmap = kwargs.get('cmap', "spot")
        p = self.lv.points(name, **kwargs)
        p.vertices(position)
        p.values(value, "v")
        p["colourby"] = "v"

        if 'vmin' in kwargs and 'vmax' in kwargs:
            logger.info('vmin {} and vmax {}'.format(kwargs['vmin'],kwargs['vmax']))
            p.colourmap(cmap, range=(kwargs['vmin'],kwargs['vmax']))
        else:
            p.colourmap(cmap)

    def add_fold(self, fold, **kwargs):
        """
        Draw the vector components of the fold at the locations

        Parameters
        ----------
        fold - fold object
        locations - numpy array of xyz

        Returns
        -------

        """
        locations = kwargs.get('locations', None)
        if locations is None:
            x = np.linspace(self.bounding_box[0, 0], self.bounding_box[1, 0], self.nsteps[0])
            y = np.linspace(self.bounding_box[0, 1], self.bounding_box[1, 1], self.nsteps[1])
            z = np.linspace(self.bounding_box[1, 2], self.bounding_box[0, 2], self.nsteps[2])
            xx, yy, zz = np.meshgrid(x, y, z, indexing='ij')
            locations = np.array([xx.flatten(), yy.flatten(), zz.flatten()]).T
        r2r, fold_axis, dgz = fold.get_deformed_orientation(locations)
        self.add_vector_data(locations, r2r, fold.name + '_direction', colour='red')
        self.add_vector_data(locations, fold_axis, fold.name + '_axis', colour='black')
        self.add_vector_data(locations, dgz, fold.name + '_norm', colour='green')

    def interactive(self, popout=False):
        """
        Runs the lavavu viewer as either a jupyter notebook
        inline interactive viewer or as a separate window

        Returns
        -------

        """
        if is_notebook() and popout is False:
            self.lv.control.Panel()
            self.lv.control.ObjectList()
            self.lv.control.show()
        if not is_notebook() or popout:
            self.lv.control.Panel()
            self.lv.control.ObjectList()
            self.lv.interactive()


    def set_zscale(self,zscale):
        """ Set the vertical scale for lavavu

        just a simple wrapper for lavavu modelscale([xscale,yscale,zscale])

        Parameters
        ----------
        zscale : float
            vertical scale
        """
        self.lv.modelscale([1,1,zscale])

    def set_viewer_rotation(self, rotation):
        """
        Set the viewer rotation given a list of rotations x,y,z

        Parameters
        ----------
        rotation numpy array of 3 rotation

        Returns
        -------

        """
        self.lv.rotate(rotation)

    def save(self, fname, **kwargs):
        """
        Calls lavavu.Viewer.image to save the viewer current state as an image

        Parameters
        ----------
        fname - file name string including relative path
        kwargs - optional kwargs to give to lavavu e.g. transparent, resolution

        Returns
        -------

        """
        self.lv.image(fname, **kwargs)

    def display(self, fname=None, **kwargs):
        """
        Calls the lv object display function. Shows a static image of the viewer inline.

        Returns
        -------

        """
        if fname:
            self.lv.image(fname, **kwargs)
            
        self.lv.display()

    def image(self, name, **kwargs):
        """
        Calls the lv object image function to save the display state

        Parameters
        ----------
        name : string
            name of the image file to save
        kwargs

        Returns
        -------

        """
        self.lv.image(name)

    def rotatex(self, r):
        """
        Rotate the viewer in the x plane

        Parameters
        ----------
        r : double
            degrees to rotate, can be +ve or -ve

        Returns
        -------

        """
        self.lv.rotatex(r)

    def rotatey(self, r):
        """
        Rotate the viewer in the Y plane

        Parameters
        ----------
        r : double
            degrees to rotate, can be +ve or -ve

        Returns
        -------

        """
        self.lv.rotatey(r)

    def rotatez(self, r):
        """
        Rotate the viewer in the z plane

        Parameters
        ----------
        r : double
            degrees to rotate, can be +ve or -ve

        Returns
        -------

        """
        self.lv.rotatez(r)

    def rotate(self, r):
        """
        Rotate by a vector of rotation angles

        Parameters
        ----------
        r : list/numpy array
            a vector of rotations

        Returns
        -------

        """
        self.lv.rotate(r)

    @property
    def rotation(self):
        """Accessor for the viewer rotation
        Returns
        -------
        list
            x,y,z rotations
        """
        return self.lv['xyzrotate']
    
    @rotation.setter
    def rotation(self,xyz):
        """Set the rotation of the viewer

        Parameters
        ----------
        xyz : list like
            x y z rotations
        """
        self.lv.rotation(xyz)

