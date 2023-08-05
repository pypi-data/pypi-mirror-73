import pandas as pd
from humanizationdb.utils.exceptions import AnnotationMissing
from abdesign.core.igobject import IgObject
import uuid
from datetime import datetime

class MetaEntry:
    """Class which guarantees consistency of meta table entries
    """
    def __init__(self, meta_key=None, ig_object=None, **kwargs):
        self._meta_key = meta_key
        self._ig_object = ig_object
        self._seq = self.ig_object.sequence if ig_object else None
        self._chain_type = self.ig_object.chain_type if ig_object else None
        self._iso_type = self.ig_object.iso_type if ig_object else None
        self._species = self.ig_object.species if ig_object else None
        self._germline = 'unknown'
        self._disease = None
        self._v_gene = 'unknown'
        self._j_gene = 'unknown'
        self._origin = 'unknown'
        _allowed_params = ['ig_object', 'sequence','chain_type','iso_type','species','germline', 'disease', 'v_gene', 'j_gene', 'origin', 'origin']
        [setattr(self, key, value) for key, value in kwargs.items() if key in _allowed_params]

    @property
    def meta_key(self):
        return self._meta_key

    @meta_key.setter
    def meta_key(self, mk):
        if mk is None:
            self._meta_key = create_uuid()
        else:
            if is_valid_uuid(mk):
                self._meta_key = mk
            else:
                raise ValueError("Invalid UUID.")

    @property
    def ig_object(self):
        return self._ig_object

    @ig_object.setter
    def ig_object(self, igo):
        if isinstance(igo, IgObject):
            self._ig_object = igo
        else:
            raise TypeError("Incorrect format")

    @property
    def sequence(self):
        return self._seq

    @sequence.setter
    def sequence(self, seq):
        self._seq = seq

    @property
    def chain_type(self):
        return self._chain_type

    @chain_type.setter
    def chain_type(self, ct):
        self._chain_type = ct

    @property
    def iso_type(self):
        return self._iso_type

    @iso_type.setter
    def iso_type(self, it):
        self._iso_type = it

    @property
    def species(self):
        return self._species

    @species.setter
    def species(self, spec):
        self._species = spec

    @property
    def germline(self):
        return self._germline

    @germline.setter
    def germline(self, germ):
        self._germline = germ

    @property
    def disease(self):
        return self._disease

    @disease.setter
    def disease(self, dis):
        self._disease = dis

    @property
    def v_gene(self):
        return self._v_gene

    @v_gene.setter
    def v_gene(self, vg):
        self._v_gene = vg

    @property
    def j_gene(self):
        return self._j_gene

    @j_gene.setter
    def j_gene(self, jg):
        self._j_gene = jg

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, pb):
        self._origin = pb

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, org):
        self._origin = org


    def __str__(self):
        return f"MetaEntry(\n\t{self.ig_object},\n\t{self.meta_key},\n\t{self.sequence},\n\t{self.chain_type},\n\t{self.iso_type},\n\t{self.species},\n\t{self.germline},\n\t{self.disease},\n\t{self.v_gene},\n\t{self.j_gene},\n\t{self.origin})"

    def get_meta_data(self):
        """Function that returns tuple with meta data

        Returns
        -------
        tuple
            Tuple containing all attributes that are necassary for DB insertion
        """
        return (self._meta_key, self.sequence, self.chain_type, self.iso_type, self.germline, self.species, self.disease, self.v_gene, self.j_gene, self.origin)

    def get_annotation_data(self):
        """Function that returns annotation data for db entry
        """
        if self.ig_object:
            if self.ig_object.annotation is not None:
                #self.ig_object.annotation = self.ig_object.annotation.get_level_values('annotation_type')
                for entry in self.ig_object.annotation.itertuples():
                    if entry.extension != None:
                        new_position = str(entry.Index[1])+str(entry.extension)
                        yield AnnotationEntry(self._meta_key,annotation_type=entry.Index[0], position=new_position, amino_acid = entry.amino_acid, chain=entry.chain, region=entry.cdr)

                    else:
                    # GET ANNOTATION TYPE HERE
                        yield AnnotationEntry(self._meta_key,annotation_type=entry.Index[0], position=entry.Index[1], amino_acid = entry.amino_acid, chain=entry.chain, region=entry.cdr)
            else:
                raise AnnotationMissing("Please provide annotation data (Dataframe).")
        else:
            return []

    def to_line(self, settedMetaKey):
        self.meta_key = settedMetaKey
        returnLine = "|".join([ self.meta_key,
                                self.sequence,
                                self.chain_type,
                                self.iso_type,
                                self.germline,
                                self.species,
                                self.disease,
                                self.v_gene,
                                self.j_gene,
                                self.origin,
                                str(datetime.now())])
        returnLine +="\n"
        return returnLine



class AnnotationEntry:
    """Class which guarantees consistency in annotation tables
    """
    def __init__(self, meta_key, annotation_type, position=None,amino_acid=None,chain=None,region=None):
        self._meta_key = meta_key
        self._annotation_type = annotation_type
        self._position = position
        self._amino_acid = amino_acid
        self._chain = chain
        self._region = region

    @property
    def meta_key(self):
        return self._meta_key

    @meta_key.setter
    def meta_key(self, mk):
        self._meta_key = mk

    @property
    def annotation_type(self):
        return self._annotation_type

    @annotation_type.setter
    def annotation_type(self, annotype):
        self._annotation_type = annotype

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, pos):
        try:
            pos = int(pos)
        except ValueError:
            raise ValueError("Position must be of type integer.")
        self._position = pos

    @property
    def amino_acid(self):
        return self._amino_acid

    @amino_acid.setter
    def amino_acid(self, aa):
        self._amino_acid = aa

    @property
    def chain(self):
        return self._chain

    @chain.setter
    def chain(self, ch):
        self._chain = ch

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, reg):
        self._region = reg

    def __str__(self):
        return f"AnnotationEntry(\n\t,{self._meta_key}\n\t,{self.position}\n\t,{self.amino_acid}\n\t,{self.chain}\n\t,{self.region}\n\t)"

    def return_insert_tuple(self):
        return (self._meta_key,self.position,self.amino_acid,self.chain,self.region)

def create_uuid():
    """Function to create UUID

    Returns
    -------
    string
        UUID
    """
    uid = uuid.uuid4()
    return uid


def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.

    Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}

    Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.

    Examples
    --------
    is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a') --> True
    is_valid_uuid('c9bf9e58') --> False
    """
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
    except ValueError:
        return False

    return str(uuid_obj) == uuid_to_test