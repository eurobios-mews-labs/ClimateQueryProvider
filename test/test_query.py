# Copyright 2023 Eurobios
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from cqpro.query_data import retriever


path = 'data/'
file_name = "2m_temperature.nc"

r = retriever(path=path, file_name=file_name)
df = r.get_data(45, -3, '2020-09-01 23:00:00', '2020-09-02 23:00:00')

print(r._get_history_range())
print(r._get_grid_range())
print(r._get_var_name())

print(df)
