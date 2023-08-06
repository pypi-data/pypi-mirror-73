import numpy as np
from ..primitives.dose import *
from ..primitives.dosebag import DoseBag
from ..primitives.dose_converter import DoseConverter


class LinearQuadratic():
    """Linear quadratic model.
    SF = exp(-a*dose -beta*dose^2) = exp(-a*dose*(1 + dose/ab_ratio)),
    where ab_ratio = alpha/beta

    """

    def __repr__(self) -> str:
        return f"ab_ratio={self.ab_ratio}, nfx={nfx}"

    def __init__(self, ab_ratio: Dose, nfx: int) -> None:
        """
        LinearQuadratic ctor.

        :param ab_ratio: Dose.
        :param nfx: Number of fractions. A number from 1...+Inf.
        """
        if not isinstance(ab_ratio, Dose):
            raise ValueError('ab_ratio must be type(Dose)')
        if not isinstance(nfx, int) and nfx < 1:
            raise ValueError('nfx must be an int value from 1..+inf')
        self.nfx = nfx
        self.ab_ratio = ab_ratio

    def suvival_fraction(self, dose: DoseBag, alpha: float) -> float:
        """
        It calculates the survival fraction after the delivery of dose in nfx fractions. It assumes that the delivered
        dose is homogeneous to the cell with alpha radiosensetivity.

        :param alpha: Cells radiosensetivity.
        :param dose: Physical dose array.
        :return: Survival fraction
        """

        if isinstance(dose, DoseBag):
            return np.exp(-alpha * self.eqd_zero(dose).data)

    def _is_different_units(self, total_dose: DoseBag, ab_ratio):
        return total_dose.unit != ab_ratio.unit

    def eqd_zero(self, total_dose: DoseBag) -> DoseBag:
        if not isinstance(total_dose, DoseBag):
            raise ValueError('total dose must be type DoseBag')

        if total_dose.dose_type != DoseType.PHYSICAL_DOSE:
            raise ValueError('total dose must be in PHYSICAL_DOSE')

        if self._is_different_units(total_dose, self.ab_ratio):
            raise ValueError('total_dose units and ab_ratio units must be the same')

        eqd0 = total_dose.data * (1.0 + (total_dose.data / self.nfx / self.ab_ratio.value))
        return DoseBag.create(data=eqd0, unit=total_dose.unit, dose_type=DoseType.EQD0,
                              param_dict={'ab_ratio': self.ab_ratio})

    def eqd_two(self, total_dose: DoseBag) -> DoseBag:
        if not isinstance(total_dose, DoseBag):
            raise ValueError('total dose must be type DoseBag')

        if total_dose.dose_type != DoseType.PHYSICAL_DOSE:
            raise ValueError('total dose must be in PHYSICAL_DOSE')

        if self._is_different_units(total_dose, self.ab_ratio):
            raise ValueError('total_dose units and ab_ratio units must be the same')

        doses_in_eqd0 = self.eqd_zero(total_dose)
        return DoseConverter.to_eqd2_from_eqd0(doses_in_eqd0)
