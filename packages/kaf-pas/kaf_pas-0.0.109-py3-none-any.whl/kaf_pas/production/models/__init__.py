from isc_common.number import StrToInt
from kaf_pas.system.models.contants import Contants

p_id = StrToInt(Contants.objects.get(code='audo_top_level').value)
