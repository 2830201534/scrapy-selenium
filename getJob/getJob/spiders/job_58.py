import json
import re

import scrapy
from getJob.items import GetjobItem
import brotli


class Job58Spider(scrapy.Spider):
    name = 'job_58'
    # allowed_domains = ['xxx']
    start_urls = [
        'https://www.58.com/changecity.html?catepath=job.shtml&catename=%E6%8B%9B%E8%81%98%E4%BF%A1%E6%81%AF&fullpath=9224&PGTID=0d202408-0019-edf3-4071-f0381bf7c1bc&ClickID=3']
    # 城市列表
    cityGroup = [['阿拉尔', '9545', 'A', '9539'], ['安宁', '547', 'A', '547'], ['安溪', '7100', 'A', '7100'],
                 ['安陆', '3442', 'A', '3442'], ['安丘', '370', 'A', '370'], ['鞍山', '523', 'A', '523'],
                 ['阿勒泰', '18804', 'A', '18837'], ['安阳', '1096', 'A', '1096'], ['安庆', '3251', 'A', '3251'],
                 ['安康', '3157', 'A', '3157'], ['中国澳门', '9384', 'A', '9399'], ['阿克苏', '9510', 'A', '9499'],
                 ['阿坝', '9814', 'A', '9817'], ['阿里', '9686', 'A', '9678'], ['阿拉善盟', '10078', 'A', '10083'],
                 ['安顺', '7458', 'A', '7468'], ['安吉', '836', 'A', '836'], ['安岳', '6806', 'A', '6806'],
                 ['白银', '10307', 'B', '10304'], ['北京', '1', 'B', '1'], ['博罗', '726', 'B', '726'],
                 ['北票', '10105', 'B', '10109'], ['北流', '9151', 'B', '9168'], ['博兴', '949', 'B', '949'],
                 ['霸州', '775', 'B', '775'], ['博白', '9154', 'B', '9173'], ['保定', '424', 'B', '424'],
                 ['包头', '801', 'B', '801'], ['滨州', '944', 'B', '944'], ['宝鸡', '2044', 'B', '2044'],
                 ['保亭', '10367', 'B', '10367'], ['白沙', '10375', 'B', '10380'], ['蚌埠', '3470', 'B', '3470'],
                 ['本溪', '5845', 'B', '5845'], ['白城', '5918', 'B', '5918'], ['亳州', '2329', 'B', '2329'],
                 ['保山', '2390', 'B', '2390'], ['巴音郭楞', '9533', 'B', '9530'], ['巴中', '9808', 'B', '9811'],
                 ['博尔塔拉', '9539', 'B', '9529'], ['巴彦淖尔市', '10063', 'B', '10070'], ['白山', '10177', 'B', '10179'],
                 ['毕节', '10553', 'B', '10564'], ['百色', '10506', 'B', '10513'], ['北海', '10510', 'B', '10536'],
                 ['宝应县', '14451', 'B', '14486'], ['慈溪', '5334', 'C', '5334'], ['沧县', '659', 'C', '659'],
                 ['长兴', '834', 'C', '834'], ['楚雄', '2393', 'C', '2393'], ['慈利', '6791', 'C', '6791'],
                 ['茌平', '887', 'C', '887'], ['常宁', '921', 'C', '921'], ['长岭', '9062', 'C', '9084'],
                 ['赤壁', '9619', 'C', '9623'], ['桂阳', '5699', 'C', '5699'], ['长宁', '7148', 'C', '7148'],
                 ['岑溪', '2119', 'C', '2119'], ['成都', '102', 'C', '102'], ['长沙', '414', 'C', '414'],
                 ['重庆', '37', 'C', '37'], ['昌乐', '373', 'C', '373'], ['昌邑', '372', 'C', '372'],
                 ['长春', '319', 'C', '319'], ['磁县', '591', 'C', '591'], ['常州', '463', 'C', '463'],
                 ['沧州', '652', 'C', '652'], ['昌吉', '8572', 'C', '8582'], ['澄迈', '10316', 'C', '10331'],
                 ['赤峰', '6700', 'C', '6700'], ['常德', '872', 'C', '872'], ['郴州', '5695', 'C', '5695'],
                 ['承德', '6760', 'C', '6760'], ['长治', '6921', 'C', '6921'], ['长葛', '9329', 'C', '9344'],
                 ['昌都', '9636', 'C', '9648'], ['朝阳', '10102', 'C', '10106'], ['巢湖', '10224', 'C', '10229'],
                 ['池州', '10254', 'C', '10260'], ['滁州', '10260', 'C', '10266'], ['潮州', '10456', 'C', '10461'],
                 ['崇左', '10514', 'C', '10524'], ['苍南', '7579', 'C', '7576'], ['曹县', '5638', 'C', '5638'],
                 ['长垣', '5936', 'C', '5936'], ['定边', '5948', 'D', '5948'], ['东台', '615', 'D', '615'],
                 ['丹阳', '648', 'D', '648'], ['德清', '835', 'D', '835'], ['东海', '2147', 'D', '2147'],
                 ['德阳', '2373', 'D', '2373'], ['大理', '2398', 'D', '2398'], ['东至', '10256', 'D', '10262'],
                 ['敦煌', '10384', 'D', '10390'], ['东阳', '536', 'D', '536'], ['大竹', '9805', 'D', '9806'],
                 ['东平', '692', 'D', '692'], ['灯塔', '2071', 'D', '2071'], ['大悟', '3437', 'D', '3437'],
                 ['邓州', '595', 'D', '595'], ['东明', '5641', 'D', '5641'], ['东莞', '413', 'D', '413'],
                 ['大连', '147', 'D', '147'], ['德州', '728', 'D', '728'], ['当阳', '865', 'D', '865'],
                 ['东营', '623', 'D', '623'], ['大庆', '375', 'D', '375'], ['定州', '8408', 'D', '8398'],
                 ['大兴安岭', '9875', 'D', '9878'], ['东方', '10244', 'D', '10250'], ['定安', '10297', 'D', '10303'],
                 ['儋州', '10390', 'D', '10394'], ['丹东', '3445', 'D', '3445'], ['大同', '6964', 'D', '6964'],
                 ['迪庆', '9417', 'D', '9432'], ['德宏', '9422', 'D', '9437'], ['达州', '9799', 'D', '9799'],
                 ['定西', '10320', 'D', '10322'], ['大丰', '11254', 'D', '11279'], ['恩施', '2302', 'E', '2302'],
                 ['鄂州', '9702', 'E', '9709'], ['鄂尔多斯', '2037', 'E', '2037'], ['府谷', '5945', 'F', '5945'],
                 ['阜阳', '2325', 'F', '2325'], ['丰城', '5711', 'F', '5711'], ['福安', '7971', 'F', '7969'],
                 ['浮梁', '9049', 'F', '9071'], ['福鼎', '7972', 'F', '7970'], ['扶余', '9063', 'F', '9085'],
                 ['分宜', '10114', 'F', '10118'], ['范县', '7285', 'F', '7285'], ['阜宁', '620', 'F', '620'],
                 ['凤城', '3450', 'F', '3450'], ['福州', '304', 'F', '304'], ['佛山', '222', 'F', '222'],
                 ['抚顺', '5722', 'F', '5722'], ['阜新', '10093', 'F', '10097'], ['抚州', '10138', 'F', '10134'],
                 ['防城港', '10530', 'F', '10539'], ['肥城', '690', 'F', '690'], ['广州', '3', 'G', '3'],
                 ['赣州', '2363', 'G', '2363'], ['广安', '2381', 'G', '2381'], ['固原', '2421', 'G', '2421'],
                 ['广水', '9631', 'G', '9657'], ['谷城', '899', 'G', '899'], ['高平', '3354', 'G', '3354'],
                 ['格尔木', '9908', 'G', '9904'], ['高安', '5712', 'G', '5712'], ['桂平', '6774', 'G', '6774'],
                 ['固始', '8676', 'G', '8698'], ['冠县', '890', 'G', '890'], ['高唐', '885', 'G', '885'],
                 ['固安', '5393', 'G', '12803'], ['改则', '9692', 'G', '9684'], ['贵阳', '2015', 'G', '2015'],
                 ['桂林', '1039', 'G', '1039'], ['馆陶', '8684', 'G', '8706'], ['贵港', '6770', 'G', '6770'],
                 ['广元', '9751', 'G', '9749'], ['甘孜', '9760', 'G', '9764'], ['果洛', '9940', 'G', '9936'],
                 ['甘南', '10337', 'G', '10343'], ['广饶', '627', 'G', '627'], ['公主岭', '10171', 'G', '10175'],
                 ['广汉', '8719', 'G', '8735'], ['灌云', '2148', 'G', '2148'], ['灌南', '2150', 'G', '2150'],
                 ['高密', '371', 'G', '371'], ['海门', '399', 'H', '399'], ['海安', '401', 'H', '401'],
                 ['海宁', '500', 'H', '500'], ['惠东', '725', 'H', '725'], ['华容', '830', 'H', '830'],
                 ['黄冈', '2299', 'H', '2299'], ['淮南', '2319', 'H', '2319'], ['黄山', '2323', 'H', '2323'],
                 ['河池', '2340', 'H', '2340'], ['鹤壁', '2344', 'H', '2344'], ['红河', '2394', 'H', '2394'],
                 ['海北', '9934', 'H', '9917'], ['滑县', '5405', 'H', '5405'], ['韩城', '5735', 'H', '5735'],
                 ['郓城', '5637', 'H', '5637'], ['河间', '658', 'H', '658'], ['杭州', '79', 'H', '79'],
                 ['黄骅', '657', 'H', '657'], ['桦甸', '706', 'H', '706'], ['衡东', '5693', 'H', '5693'],
                 ['海盐', '504', 'H', '504'], ['淮滨', '8680', 'H', '8702'], ['哈尔滨', '202', 'H', '202'],
                 ['海口', '2053', 'H', '2053'], ['合肥', '837', 'H', '837'], ['呼和浩特', '811', 'H', '811'],
                 ['惠州', '722', 'H', '722'], ['衡阳', '914', 'H', '914'], ['邯郸', '572', 'H', '572'],
                 ['湖州', '831', 'H', '831'], ['衡水', '993', 'H', '993'], ['鹤岗', '9039', 'H', '9061'],
                 ['黑河', '9858', 'H', '9862'], ['哈密', '7452', 'H', '7452'], ['汉中', '3163', 'H', '3163'],
                 ['淮安', '968', 'H', '968'], ['黄石', '1734', 'H', '1734'], ['中国香港', '2050', 'H', '2050'],
                 ['海拉尔', '2043', 'H', '2043'], ['菏泽', '5632', 'H', '5632'], ['怀化', '5756', 'H', '5756'],
                 ['淮北', '9342', 'H', '9357'], ['和田', '9486', 'H', '9489'], ['黄南', '9896', 'H', '9896'],
                 ['海西', '9905', 'H', '9902'], ['海东', '9921', 'H', '9909'], ['呼伦贝尔', '10035', 'H', '10039'],
                 ['葫芦岛', '10083', 'H', '10088'], ['河源', '10462', 'H', '10467'], ['贺州', '10541', 'H', '10549'],
                 ['海南', '10567', 'H', '10574'], ['和县', '10868', 'H', '10892'], ['霍邱', '11201', 'H', '11226'],
                 ['汉川', '3439', 'H', '3439'], ['海丰', '9444', 'H', '9459'], ['桓台', '7335', 'H', '7335'],
                 ['靖边', '5947', 'J', '5947'], ['金昌', '7428', 'J', '7428'], ['晋江', '297', 'J', '297'],
                 ['建湖', '618', 'J', '618'], ['靖江', '698', 'J', '698'], ['荆门', '2296', 'J', '2296'],
                 ['锦州', '2354', 'J', '2354'], ['景德镇', '2360', 'J', '2360'], ['吉安', '2364', 'J', '2364'],
                 ['嘉善', '14320', 'J', '14357'], ['京山', '9095', 'J', '9117'], ['鄄城', '5635', 'J', '5635'],
                 ['江山', '6796', 'J', '6796'], ['嘉鱼', '9620', 'J', '9624'], ['浚县', '9169', 'J', '9185'],
                 ['进贤', '677', 'J', '677'], ['句容', '650', 'J', '650'], ['巨野', '5640', 'J', '5640'],
                 ['金湖', '975', 'J', '975'], ['江阴', '100', 'J', '34984'], ['济南', '265', 'J', '265'],
                 ['济宁', '450', 'J', '450'], ['嘉兴', '497', 'J', '497'], ['江门', '629', 'J', '629'],
                 ['金华', '531', 'J', '531'], ['吉林', '700', 'J', '700'], ['揭阳', '927', 'J', '927'],
                 ['晋中', '8832', 'J', '8854'], ['济源', '9894', 'J', '9918'], ['九江', '2247', 'J', '2247'],
                 ['焦作', '3266', 'J', '3266'], ['晋城', '3350', 'J', '3350'], ['荆州', '3479', 'J', '3479'],
                 ['佳木斯', '6776', 'J', '6776'], ['鸡西', '7289', 'J', '7289'], ['嘉峪关', '10356', 'J', '10362'],
                 ['酒泉', '10381', 'J', '10387'], ['金坛', '468', 'J', '468'], ['姜堰', '697', 'J', '697'],
                 ['简阳', '6805', 'J', '6805'], ['莒县', '3180', 'J', '3180'], ['开原', '6733', 'K', '6733'],
                 ['开封', '2342', 'K', '2342'], ['开平', '634', 'K', '634'], ['昆明', '541', 'K', '541'],
                 ['克拉玛依', '2042', 'K', '2042'], ['喀什', '9311', 'K', '9326'], ['克孜勒苏', '9527', 'K', '9519'],
                 ['垦利', '11288', 'K', '11313'], ['昆山', '16', 'K', '16'], ['溧阳', '469', 'L', '469'],
                 ['莱芜', '2292', 'L', '2292'], ['六安', '2328', 'L', '2328'], ['泸州', '2372', 'L', '2372'],
                 ['丽江', '2392', 'L', '2392'], ['龙口', '233', 'L', '233'], ['乐陵', '730', 'L', '730'],
                 ['冷水江', '9460', 'L', '9470'], ['陆丰', '9443', 'L', '9456'], ['涟源', '9461', 'L', '9471'],
                 ['临清', '884', 'L', '884'], ['新安', '11192', 'L', '11217'], ['澧县', '876', 'L', '876'],
                 ['柳林', '3225', 'L', '3225'], ['梨树县', '10172', 'L', '10176'], ['利津', '628', 'L', '628'],
                 ['滦南', '7066', 'L', '7066'], ['梁山', '462', 'L', '462'], ['临邑', '739', 'L', '739'],
                 ['老河口', '895', 'L', '895'], ['鹿邑', '939', 'L', '939'], ['林州', '1101', 'L', '1101'],
                 ['兰考', '7393', 'L', '7393'], ['莱阳', '234', 'L', '234'], ['临朐', '374', 'L', '374'],
                 ['兰州', '952', 'L', '952'], ['洛阳', '556', 'L', '556'], ['廊坊', '772', 'L', '772'],
                 ['临沂', '505', 'L', '505'], ['聊城', '882', 'L', '882'], ['连云港', '2049', 'L', '2049'],
                 ['丽水', '7923', 'L', '7921'], ['临猗', '9179', 'L', '9193'], ['娄底', '9455', 'L', '9481'],
                 ['陵水', '10166', 'L', '10184'], ['六盘水', '10500', 'L', '10506'], ['吕梁', '3222', 'L', '3222'],
                 ['乐山', '3237', 'L', '3237'], ['辽阳', '2038', 'L', '2038'], ['辽源', '2501', 'L', '2501'],
                 ['拉萨', '2055', 'L', '2055'], ['临汾', '5669', 'L', '5669'], ['龙岩', '6752', 'L', '6752'],
                 ['临夏', '7112', 'L', '7112'], ['柳州', '7133', 'L', '7133'], ['漯河', '2347', 'L', '2347'],
                 ['临沧', '9407', 'L', '9422'], ['凉山', '9715', 'L', '9717'], ['林芝', '9635', 'L', '9646'],
                 ['陇南', '10409', 'L', '10415'], ['来宾', '10549', 'L', '10552'], ['莱州', '235', 'L', '235'],
                 ['临海', '407', 'L', '407'], ['灵宝', '9307', 'L', '9321'], ['乐平', '9048', 'L', '9070'],
                 ['龙海', '713', 'L', '713'], ['醴陵', '1091', 'L', '1091'], ['孟津', '7122', 'M', '7122'],
                 ['梅河口', '10160', 'M', '10162'], ['孟州', '3267', 'M', '3267'], ['弥勒', '8870', 'M', '8892'],
                 ['绵阳', '1057', 'M', '1057'], ['茂名', '679', 'M', '679'], ['明港', '8531', 'M', '8541'],
                 ['马鞍山', '2039', 'M', '2039'], ['牡丹江', '3489', 'M', '3489'], ['梅州', '9374', 'M', '9389'],
                 ['眉山', '9704', 'M', '9704'], ['南安', '293', 'N', '293'], ['南漳', '898', 'N', '898'],
                 ['南充', '2378', 'N', '2378'], ['宁国', '5645', 'N', '5645'], ['南城', '10142', 'N', '10137'],
                 ['南县', '10198', 'N', '10202'], ['宁津', '733', 'N', '733'], ['宁阳', '691', 'N', '691'],
                 ['南京', '172', 'N', '172'], ['南昌', '669', 'N', '669'], ['宁波', '135', 'N', '135'],
                 ['南宁', '845', 'N', '845'], ['南阳', '592', 'N', '592'], ['南通', '394', 'N', '394'],
                 ['宁德', '7969', 'N', '7951'], ['内江', '5928', 'N', '5928'], ['怒江', '9452', 'N', '9462'],
                 ['那曲', '9625', 'N', '9618'], ['南平', '10285', 'N', '10291'], ['沛县', '11325', 'P', '11349'],
                 ['邳州', '477', 'P', '477'], ['攀枝花', '2371', 'P', '2371'], ['平湖', '501', 'P', '501'],
                 ['磐石', '708', 'P', '708'], ['平阳', '7578', 'P', '7575'], ['平邑', '514', 'P', '514'],
                 ['平顶山', '1005', 'P', '1005'], ['盘锦', '2041', 'P', '2041'], ['萍乡', '2248', 'P', '2248'],
                 ['平凉', '7154', 'P', '7154'], ['濮阳', '2346', 'P', '2346'], ['莆田', '2429', 'P', '2429'],
                 ['普洱', '9429', 'P', '9444'], ['蓬莱', '237', 'P', '237'], ['启东', '400', 'Q', '400'],
                 ['钦州', '2335', 'Q', '2335'], ['曲靖', '2389', 'Q', '2389'], ['祁阳', '8522', 'Q', '8532'],
                 ['祁东', '5690', 'Q', '5690'], ['迁西', '7061', 'Q', '7061'], ['淇县', '9170', 'Q', '9186'],
                 ['渠县', '9806', 'Q', '9807'], ['齐河', '734', 'Q', '734'], ['沁阳', '3268', 'Q', '3268'],
                 ['清镇', '12631', 'Q', '12703'], ['栖霞', '238', 'Q', '238'], ['青岛', '122', 'Q', '122'],
                 ['泉州', '291', 'Q', '291'], ['秦皇岛', '1078', 'Q', '1078'], ['其他', '2258', 'Q', '2258'],
                 ['七台河', '9846', 'Q', '9848'], ['琼海', '10130', 'Q', '10136'], ['黔西南', '10430', 'Q', '10434'],
                 ['黔南', '10441', 'Q', '10492'], ['齐齐哈尔', '5853', 'Q', '5853'], ['衢州', '6793', 'Q', '6793'],
                 ['清远', '7303', 'Q', '7303'], ['黔东南', '9348', 'Q', '9363'], ['琼中', '10060', 'Q', '10064'],
                 ['庆阳', '10470', 'Q', '10475'], ['清徐', '10884', 'Q', '10908'], ['潜江', '9655', 'Q', '9669'],
                 ['迁安市', '284', 'Q', '284'], ['青州', '367', 'Q', '367'], ['杞县', '7389', 'Q', '7389'],
                 ['如皋', '397', 'R', '397'], ['如东', '402', 'R', '402'], ['日土', '9690', 'R', '9682'],
                 ['日照', '3177', 'R', '3177'], ['瑞安', '13894', 'R', '13951'], ['日喀则', '9587', 'R', '9615'],
                 ['荣成', '522', 'R', '522'], ['汝州', '1010', 'R', '1010'], ['仁寿', '9706', 'R', '9706'],
                 ['任丘', '656', 'R', '656'], ['乳山', '520', 'R', '520'], ['仁怀', '7628', 'R', '7624'],
                 ['安达', '6720', 'S', '6720'], ['肇东', '6721', 'S', '6721'], ['上海', '2', 'S', '2'], ['深圳', '4', 'S', '4'],
                 ['石狮', '296', 'S', '296'], ['寿光', '369', 'S', '369'], ['松原', '2315', 'S', '2315'],
                 ['三亚', '2422', 'S', '2422'], ['沙洋', '9096', 'S', '9118'], ['随县', '9633', 'S', '9660'],
                 ['商水', '936', 'S', '936'], ['上杭', '6757', 'S', '6757'], ['邵东', '6954', 'S', '6954'],
                 ['双峰', '9462', 'S', '9473'], ['射洪', '9699', 'S', '9694'], ['沙河', '755', 'S', '755'],
                 ['邵阳县', '6955', 'S', '6955'], ['松滋', '3484', 'S', '3484'], ['射阳', '621', 'S', '621'],
                 ['嵊州', '359', 'S', '359'], ['莘县', '888', 'S', '888'], ['沈丘', '942', 'S', '942'],
                 ['睢县', '1038', 'S', '1038'], ['涉县', '14005', 'S', '14059'], ['苏州', '5', 'S', '5'],
                 ['沈阳', '188', 'S', '188'], ['石家庄', '241', 'S', '241'], ['汕头', '783', 'S', '783'],
                 ['宿州', '3359', 'S', '3359'], ['绍兴', '355', 'S', '355'], ['十堰', '2032', 'S', '2032'],
                 ['顺德', '8694', 'S', '8716'], ['三门峡', '9303', 'S', '9317'], ['双鸭山', '9836', 'S', '9837'],
                 ['三沙', '13663', 'S', '13722'], ['三明', '2048', 'S', '2048'], ['韶关', '2192', 'S', '2192'],
                 ['商丘', '1029', 'S', '1029'], ['沭阳', '5772', 'S', '5772'], ['宿迁', '2350', 'S', '2350'],
                 ['绥化', '6718', 'S', '6718'], ['邵阳', '2303', 'S', '2303'], ['汕尾', '9441', 'S', '9449'],
                 ['商洛', '9851', 'S', '9854'], ['朔州', '9869', 'S', '9871'], ['石河子', '9556', 'S', '9551'],
                 ['石嘴山', '9967', 'S', '9971'], ['山南', '9578', 'S', '9576'], ['遂宁', '9695', 'S', '9688'],
                 ['上饶', '10116', 'S', '10120'], ['四平', '10167', 'S', '10171'], ['随州', '9630', 'S', '9656'],
                 ['神农架', '9597', 'S', '9605'], ['神木', '5944', 'S', '5944'], ['泗阳', '5959', 'S', '5959'],
                 ['泗洪', '5958', 'S', '5958'], ['单县', '5636', 'S', '5636'], ['三河', '776', 'S', '776'],
                 ['天长', '10267', 'T', '10273'], ['桐乡', '502', 'T', '502'], ['泰兴', '696', 'T', '696'],
                 ['天水', '8467', 'T', '8601'], ['郯城', '510', 'T', '510'], ['太康', '938', 'T', '938'],
                 ['通许', '7390', 'T', '7390'], ['天津', '18', 'T', '18'], ['太原', '740', 'T', '740'],
                 ['唐山', '276', 'T', '276'], ['塔城', '18812', 'T', '18845'], ['泰安', '686', 'T', '686'],
                 ['台州', '403', 'T', '403'], ['屯昌', '10049', 'T', '10044'], ['铜仁', '10419', 'T', '10417'],
                 ['泰州', '693', 'T', '693'], ['中国台湾', '2051', 'T', '2051'], ['铁岭', '6729', 'T', '6729'],
                 ['吐鲁番', '9464', 'T', '9475'], ['铜川', '9829', 'T', '9832'], ['图木舒克', '9563', 'T', '9559'],
                 ['通辽', '10012', 'T', '10015'], ['通化', '10157', 'T', '10159'], ['铜陵', '10279', 'T', '10285'],
                 ['天门', '9475', 'T', '9517'], ['台山', '11238', 'T', '11263'], ['桐城', '11271', 'T', '11296'],
                 ['滕州', '967', 'T', '967'], ['武穴', '7362', 'W', '7362'], ['温岭', '408', 'W', '408'],
                 ['文山', '2395', 'W', '2395'], ['乌海', '2404', 'W', '2404'], ['无为', '10227', 'W', '10232'],
                 ['无棣', '951', 'W', '951'], ['舞钢', '1011', 'W', '1011'], ['尉氏', '7391', 'W', '7391'],
                 ['武汉', '158', 'W', '158'], ['汶上', '460', 'W', '460'], ['温县', '7312', 'W', '7312'],
                 ['武义县', '14494', 'W', '14528'], ['微山', '459', 'W', '459'], ['无锡', '93', 'W', '93'],
                 ['潍坊', '362', 'W', '362'], ['乌鲁木齐', '984', 'W', '984'], ['温州', '330', 'W', '330'],
                 ['威海', '518', 'W', '518'], ['五指山', '9948', 'W', '9952'], ['文昌', '9968', 'W', '9984'],
                 ['万宁', '10011', 'W', '10022'], ['芜湖', '2045', 'W', '2045'], ['梧州', '2046', 'W', '2046'],
                 ['瓦房店', '3279', 'W', '3279'], ['渭南', '5733', 'W', '5733'], ['五家渠', '9564', 'W', '9562'],
                 ['吴忠', '9959', 'W', '9962'], ['乌兰察布', '9998', 'W', '9993'], ['武威', '10443', 'W', '10448'],
                 ['武夷山', '10737', 'W', '10761'], ['武安', '577', 'W', '577'], ['象山', '6738', 'X', '6738'],
                 ['新沂', '478', 'X', '478'], ['兴化', '699', 'X', '699'], ['西双版纳', '2397', 'X', '2397'],
                 ['孝义', '3227', 'X', '3227'], ['宣威', '7507', 'X', '7533'], ['孝昌', '3436', 'X', '3436'],
                 ['襄垣', '6928', 'X', '6928'], ['宣汉', '9803', 'X', '9804'], ['湘阴', '828', 'X', '828'],
                 ['西安', '483', 'X', '483'], ['盱眙', '976', 'X', '976'], ['香河', '5395', 'X', '5395'],
                 ['新昌', '361', 'X', '361'], ['新野', '603', 'X', '603'], ['响水', '619', 'X', '619'],
                 ['厦门', '606', 'X', '606'], ['徐州', '471', 'X', '471'], ['湘潭', '2047', 'X', '2047'],
                 ['襄阳', '891', 'X', '891'], ['新乡', '1016', 'X', '1016'], ['信阳', '8672', 'X', '8694'],
                 ['仙桃', '9723', 'X', '9736'], ['咸阳', '7453', 'X', '7453'], ['邢台', '751', 'X', '751'],
                 ['孝感', '3434', 'X', '3434'], ['西宁', '2052', 'X', '2052'], ['许昌', '977', 'X', '977'],
                 ['忻州', '3453', 'X', '3453'], ['宣城', '5633', 'X', '5633'], ['兴安盟', '9983', 'X', '9976'],
                 ['新余', '10111', 'X', '10115'], ['湘西', '10214', 'X', '10219'], ['咸宁', '9616', 'X', '9617'],
                 ['锡林郭勒', '2408', 'X', '2408'], ['新泰', '689', 'X', '689'], ['雄安新区', '111234', 'X', '26048'],
                 ['项城', '935', 'X', '935'], ['玉田', '7060', 'Y', '7060'], ['扬中', '649', 'Y', '649'],
                 ['宜都', '864', 'Y', '864'], ['阳江', '2284', 'Y', '2284'], ['永州', '2307', 'Y', '2307'],
                 ['玉林', '2337', 'Y', '2337'], ['沅江', '10197', 'Y', '10201'], ['禹城', '731', 'Y', '731'],
                 ['禹州', '979', 'Y', '979'], ['永城', '1032', 'Y', '1032'], ['永安', '2133', 'Y', '2133'],
                 ['余江', '3210', 'Y', '3210'], ['云梦', '3438', 'Y', '3438'], ['宜城', '897', 'Y', '897'],
                 ['永兴', '5701', 'Y', '5701'], ['渑池', '9308', 'Y', '9322'], ['宜阳', '11194', 'Y', '11219'],
                 ['阳谷', '886', 'Y', '886'], ['沂南', '7301', 'Y', '7301'], ['沂源', '7334', 'Y', '7334'],
                 ['伊川', '11195', 'Y', '11220'], ['永春', '7101', 'Y', '7101'], ['烟台', '228', 'Y', '228'],
                 ['余姚', '5333', 'Y', '5333'], ['扬州', '637', 'Y', '637'], ['宜昌', '858', 'Y', '858'],
                 ['盐城', '613', 'Y', '613'], ['岳阳', '821', 'Y', '821'], ['阳春', '8556', 'Y', '8566'],
                 ['阳泉', '8738', 'Y', '8760'], ['延安', '8951', 'Y', '8973'], ['鄢陵', '9101', 'Y', '9123'],
                 ['伊春', '9765', 'Y', '9773'], ['乐清', '13895', 'Y', '13950'], ['银川', '2054', 'Y', '2054'],
                 ['延边', '3184', 'Y', '3184'], ['鹰潭', '3209', 'Y', '3209'], ['玉溪', '2040', 'Y', '2040'],
                 ['运城', '5653', 'Y', '5653'], ['宜春', '5709', 'Y', '5709'], ['营口', '5898', 'Y', '5898'],
                 ['榆林', '5942', 'Y', '5942'], ['宜宾', '2380', 'Y', '2380'], ['雅安', '9676', 'Y', '9687'],
                 ['玉树', '9886', 'Y', '9888'], ['伊犁', '9465', 'Y', '9472'], ['益阳', '10193', 'Y', '10198'],
                 ['云浮', '10480', 'Y', '10485'], ['永新', '11053', 'Y', '11077'], ['义乌', '12221', 'Y', '12291'],
                 ['燕郊', '12730', 'Y', '12804'], ['永康', '537', 'Y', '537'], ['玉环', '409', 'Y', '409'],
                 ['偃师', '7121', 'Y', '7121'], ['诸暨', '357', 'Z', '357'], ['遵化市', '283', 'Z', '283'],
                 ['肇州', '382', 'Z', '382'], ['攸县', '1095', 'Z', '1095'], ['资兴', '5698', 'Z', '5698'],
                 ['钟祥', '9097', 'Z', '9119'], ['樟树', '5713', 'Z', '5713'], ['漳浦', '717', 'Z', '717'],
                 ['泽州', '3353', 'Z', '3353'], ['郑州', '342', 'Z', '342'], ['珠海', '910', 'Z', '910'],
                 ['张家口', '3328', 'Z', '3328'], ['中山', '771', 'Z', '771'], ['淄博', '385', 'Z', '385'],
                 ['株洲', '1086', 'Z', '1086'], ['枝江', '866', 'Z', '866'], ['漳州', '710', 'Z', '710'],
                 ['湛江', '791', 'Z', '791'], ['肇庆', '901', 'Z', '901'], ['枣庄', '961', 'Z', '961'],
                 ['舟山', '8470', 'Z', '8481'], ['章丘', '8658', 'Z', '8680'], ['赵县', '9026', 'Z', '9048'],
                 ['诸城', '9124', 'Z', '9146'], ['遵义', '7624', 'Z', '7620'], ['镇江', '645', 'Z', '645'],
                 ['周口', '933', 'Z', '933'], ['正定', '3198', 'Z', '3198'], ['驻马店', '1067', 'Z', '1067'],
                 ['庄河', '3306', 'Z', '3306'], ['自贡', '6745', 'Z', '6745'], ['张家界', '6788', 'Z', '6788'],
                 ['资阳', '6803', 'Z', '6803'], ['昭通', '9394', 'Z', '9409'], ['中卫', '9949', 'Z', '9951'],
                 ['张掖', '10449', 'Z', '10454'], ['张北', '11176', 'Z', '11201'], ['邹平', '946', 'Z', '946'],
                 ['邹城', '455', 'Z', '455'], ['涿州', '428', 'Z', '428'], ['招远', '3325', 'Z', '3325'],
                 ['枣阳', '896', 'Z', '896']]

    City_Code_Page_list = []  # 存储每个城市的代码及分页数

    # 登录请求
    def start_requests(self):
        log_url = "https://passport.58.com/login/?path=https%3A%2F%2Fcs.58.com%2Fjob.shtml%3Futm_source%3Dmarket%26spm%3Du-2d2yxv86y3v43nkddh1.BDPCPZ_BT%26PGTID%3D0d100000-0019-e329-e4d5-4bb0d0c6e79f%26ClickID%3D4&source=58-homepage-pc&PGTID=0d202408-0019-ed52-7dcd-8033768af605&ClickID=2"
        yield scrapy.Request(url=log_url)

    def parse(self, response):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse_city)

    # 城市切换页面解析
    def parse_city(self, response):
        cityHref_list = response.xpath("//div[@class='content-cities']/a/@href").extract()
        cityName_list = response.xpath("//div[@class='content-cities']/a/text()").extract()
        # print(response)
        for index in range(0, 1):
            print("当前正在获取城市 --- {}  链接 --- {}".format(cityName_list[index], cityHref_list[index]))
            # 发起寻找城市主板块请求
            url = "https:" + cityHref_list[index]
            print("城市主板块：", url)
            yield scrapy.Request(url=url, callback=self.parse_findJob,
                                 meta={"cityHead_url": url, "cityName": cityName_list[index]})

    # 处理城市主板块请求
    def parse_findJob(self, response):
        # 获取城市招聘专区url
        city_detail_url = response.xpath("//li[@id='zpNav']/a[@class='topIco']/@href").extract_first()
        print("城市招聘专区：", city_detail_url)
        # 经过测试得知，city_detail_url如果是 /job.shtml 那么最大页码数就是 175,这种情况就不发起请求了
        # url = "https://entdict.58.com/enterpriselibrary/inrecruitinginfos?searchType=0&qid=11428937071&cityid=0&cateid=&pageindex=1&adsCode=399d96d67393486586cee2eb41a32a70&t=1658192769746"
        url = "https://entdict.58.com/enterpriselibrary/enterpriselist?from=pc&cityid={}&pageindex={}&tagids=58523_0%7C900000_0%7C2147483647_0&t=1658209845754"
        if city_detail_url == "/job.shtml":
            # 存储到列表中
            for city in self.cityGroup:
                if response.meta['cityName'] in city:
                    # temp = [city[0], city[3], 175]
                    # self.City_Code_Page_list.append(temp)
                    print("normal --- 【{}】 最大页码为：{}".format(response.meta['cityName'], 175))
                    # 发起获取企业id请求
                    for index in range(1, 3):
                        print("正在获取【{}】第 {} 页企业id".format(city[0], index))
                        yield scrapy.Request(url=url.format(city[3], index), callback=self.parse_qid,
                                             meta={"cityData": [city[0], city[3], index]})
        else:
            # 对城市url发起请求 -- 获取其它城市最大页码
            yield scrapy.Request(url=response.meta['cityHead_url'] + city_detail_url, callback=self.parse_cityDetail,
                                 meta={"cityName": response.meta['cityName']})

    # 处理城市url请求 -- 获取其它城市最大页码
    def parse_cityDetail(self, response):
        # 获取企业招聘url
        # https://entdict.58.com/enterpriselibrary/index?from=pc_zpsy
        company_url = response.xpath("//div[@class='tabsbar']/a[3]/@href").extract_first()
        # 对企业url 发起请求,获取其它城市最大页码
        yield scrapy.Request(url="https:" + company_url, callback=self.parse_companyDetail,
                             meta={"cityName": response.meta['cityName'], "company_url": company_url})

    # 处理企业url请求,获取其它城市最大页码完成
    def parse_companyDetail(self, response):
        print("处理企业url请求,获取其它城市最大页码")
        MAX_PAGE = 1
        page_list = response.xpath('//span[@class="t-g-page-item active-false"]/text()').extract()
        for page in page_list:
            if page.isdigit():
                MAX_PAGE = int(page)
        print("no noraml ---【{}】 最大页码为：{}".format(response.meta['cityName'], MAX_PAGE))
        url = "https://entdict.58.com/enterpriselibrary/enterpriselist?from=pc&cityid={}&pageindex={}&tagids=58523_0%7C900000_0%7C2147483647_0&t=1658209845754"
        # 存储到列表中
        for city in self.cityGroup:
            if response.meta['cityName'] in city:
                # temp = [city[0], city[1], MAX_PAGE]
                # self.City_Code_Page_list.append(temp)
                for index in range(1, 3):
                    print("正在获取【{}】第 {} 页企业id".format(city[0], index))
                    yield scrapy.Request(url=url.format(city[3], index), callback=self.parse_qid,
                                         meta={"cityData": [city[0], city[1], index]})

        # print(self.City_Code_Page_list)

    # 处理企业id请求
    def parse_qid(self, response):
        print("正在处理企业id请求")
        # 清洗返回的数据，取出json数据
        data = response.body.decode('utf-8')
        rex = re.compile(r'.*pre-wrap;">(.*)</pre>')
        data = rex.findall(data)
        # print("正则清洗后的数据如下：")
        # print(type(data))
        # print(data[0])
        responseData = json.loads(data[0])
        # 判断数据是否存在
        for temp in responseData.values():
            # print(temp)
            if isinstance(temp, list):
                for dict_id in temp:
                    if "qid" in dict_id.keys():
                        # 发起企业详情页数据请求
                        url = "https://entdict.58.com/enterpriselibrary/inrecruitinginfos?searchType=0&qid={}&cityid={" \
                              "}&pageindex=1"
                        # print("发起【{}】企业第 {} 页详情数据请求".format(response.meta['cityData'][0], response.meta['cityData'][2]))
                        print("发起企业详情页数据请求")
                        yield scrapy.Request(url=url.format(dict_id['qid'], response.meta['cityData'][1]),
                                             callback=self.parse_company, meta={'cityData': response.meta['cityData']})

    # 处理企业详情页请求
    def parse_company(self, response):
        print("正在处理企业详情页请求")
        responseData = re.compile(r'.*pre-wrap;">(.*)</pre>').findall(response.body.decode('utf-8'))[0]
        responseData = json.loads(responseData)
        # print(responseData)
        try:
            for tempData in responseData.values():
                if isinstance(tempData, dict):
                    if "firstData" in tempData.keys():
                        for data in tempData['firstData']['data']:
                            detail_url = data['pcDetailUrl']  # 职位详情页url
                            if "identity" in data.keys():
                                identity = data['identity']  # 招聘人身份
                            else:
                                identity = None
                            userName = data['userName']  # 招聘人名称
                            userId = data['userId']  # 招聘人id
                            state = data['state']  # 状态
                            infoId = data['infoId']  # 招聘信息id
                            temp = [detail_url, identity, userName, userId, state, infoId]
                            # print(temp)
                            print("【{}】发起职位详情页请求 --- {}".format(response.meta['cityData'][0], temp[0]))
                            # 发起职位详情页请求
                            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={"partData": temp})

                    if "secondData" in tempData.keys():
                        for data in tempData['secondData']['data']:
                            detail_url = data['pcDetailUrl']  # 职位详情页url
                            if "identity" in data.keys():
                                identity = data['identity']  # 招聘人身份
                            else:
                                identity = None
                            userName = data['userName']  # 招聘人名称
                            userId = data['userId']  # 招聘人id
                            state = data['state']  # 状态
                            infoId = data['infoId']  # 招聘信息id
                            temp = [detail_url, identity, userName, userId, state, infoId]
                            # print(temp)
                            print("【{}】发起职位详情页请求 --- {}".format(response.meta['cityData'][0], temp[0]))
                            # 发起职位详情页请求
                            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={"partData": temp})
        except Exception as ex:
            print(ex)

    # 处理职位详情页请求
    def parse_detail(self, response):
        print("正在处理职位详情页请求")
        partData = response.meta['partData']
        updateTime = response.xpath("//span[@class='pos_base_num pos_base_update']/span//text()").extract()
        visitors = response.xpath("//span[@class='pos_base_num pos_base_browser']/i/text()").extract_first()  # 浏览人数
        apply = response.xpath("//span[@class='pos_base_num pos_base_apply']/span/text()").extract_first()  # 申请人数
        pos_title = response.xpath("//span[@class='pos_title']/text()").extract_first()  # 职业名称
        pos_name = response.xpath("//span[@class='pos_name']/text()").extract_first()  # 职位简单说明
        pos_salary = response.xpath("//span[@class='pos_salary']/text() | //span[@class='pos_salary daiding']/text()").extract_first()
        pos_welfare = response.xpath("//div[@class='pos_welfare']/span/text()").extract()  # 职位福利
        pos_num = response.xpath(
            "//div[@class='pos_base_condition']/span[@class='item_condition pad_left_none']/text()").extract_first()  # 招聘人数
        pos_edu = response.xpath(
            "//div[@class='pos_base_condition']/span[@class='item_condition']/text()").extract_first()  # 学历要求
        pos_year = response.xpath("//div[@class='pos_base_condition']/span[@class='item_condition "
                                  "border_right_None']/text()").extract_first()  # 经验要求
        work_city = response.xpath("//div[@class='pos-area']/span[1]/span/text()").extract()  # 工作城市
        detail_address = response.xpath("//div[@class='pos-area']/span[2]/text()").extract_first()  # 工作城市
        company_name = response.xpath("//div[@class='baseInfo_link']/a/text()").extract_first()  # 公司名称
        company_category = response.xpath("//a[@class='comp_baseInfo_link']/text()").extract_first()  # 公司经营范围
        company_scale = response.xpath("//p[@class='comp_baseInfo_scale']/text()").extract_first()  # 公司规模（人数）

        item = GetjobItem()
        item['updateTime'] = updateTime
        item['visitors'] = visitors
        item['apply'] = apply
        item['pos_title'] = pos_title
        item['pos_name'] = pos_name
        item['pos_salary'] = pos_salary
        item['pos_welfare'] = pos_welfare
        item['pos_num'] = pos_num
        item['pos_edu'] = pos_edu
        item['pos_year'] = pos_year
        item['work_city'] = work_city
        item['detail_address'] = detail_address
        item['company_name'] = company_name
        item['company_category'] = company_category
        item['company_scale'] = company_scale
        item['detail_url'] = partData[0]
        item['identity'] = partData[1]
        item['userName'] = partData[2]
        item['userId'] = partData[3]
        item['state'] = partData[4]
        item['infoId'] = partData[5]

        yield item
