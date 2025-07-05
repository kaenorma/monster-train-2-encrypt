# 简易修改

找到 %USERPROFILE%\AppData\LocalLow\Shiny Shoe\MonsterTrain2\saves 文件夹下的save-singlePlayer.json文件,

找到gold":{"_values":[210,123,121,230,232,189,69,64,112,33,52,204,184,16,26,64]}

把"_values"后那些数字改了就行

给几个常用值:
1加密:
[254, 248, 97, 184, 253, 75, 208, 63, 129, 3, 207, 35, 1, 218, 231, 63]
20加密:
[141, 229, 79, 251, 176, 56, 38, 64, 115, 26, 176, 4, 79, 199, 33, 64]
50加密:
[92, 164, 150, 237, 93, 29, 217, 63, 183, 210, 36, 68, 197, 205, 72, 64]
100加密:
[210, 45, 58, 24, 29, 47, 79, 64, 46, 210, 197, 231, 226, 208, 66, 64]
200加密:
[145, 180, 158, 224, 135, 183, 82, 64, 111, 75, 97, 31, 120, 72, 95, 64]
500加密:
[154, 141, 243, 237, 232, 80, 118, 64, 204, 228, 24, 36, 46, 222, 97, 64]
1000加密:
[220, 246, 50, 245, 174, 17, 122, 64, 146, 132, 102, 133, 40, 55, 130, 64]
5000加密:
[61, 17, 14, 70, 91, 34, 148, 64, 98, 247, 248, 92, 210, 254, 172, 64]
10000加密:
[103, 241, 174, 166, 83, 252, 179, 64, 153, 14, 81, 89, 172, 19, 179, 64]


# 正文

怪物火车2采用**ObfuscatedNumber**类混淆数据, 这里提供了加解密的脚本

数据存档在[%USERPROFILE%\AppData\LocalLow\Shiny Shoe\MonsterTrain2\saves\save-singlePlayer.json]()

其中有5项是加密的

* 龙之宝藏上限:"dragonsHoardCap" 
* 龙之宝藏:dragonsHoard 
* 血量:towerHP 
* 血量上限:  "maxTowerHP"
* 金币: gold

形如

```json
"gold":{"_values":[210,123,121,230,232,189,69,64,112,33,52,204,184,16,26,64]}
```



加密思路是: 

1. 随机拆分 原数值`double value`为`num`和`(value-num)`2个数
2. 将2个数转为byte并copy到array中, *比如15.61=0x(04 77 26 a0 81 3b 2f 40)=>(4,119,38,160,129,59,47,64)*

```
#整体流程伪代码

double value=10000.0 #原数值
#拆分为2个数
double num=15.61 #另一个数值(value-num)=9984.24
#2个数的byte形式数组进行拼接并存储
byte[] num_1_arr= [4,119,38,160,129,59,47,64]
byte[] num_2_arr=[63,98,246,151,31,128,195,64]

byte[] 最终存储_arr = concat(num_1_array,num_2_arr) = [4,119,38,160,129,59,47,64,63,98,246,151,31,128,195,64]
```



解密思路是: 将前8字节和后8字节分别转换为 `double`，然后相加得到原始值。

```

#整体流程伪代码

# 存档中的数组
byte[] 最终存储_arr = concat(num_1_array,num_2_arr) = [4,119,38,160,129,59,47,64,63,98,246,151,31,128,195,64]

# 拆分为2个数的byte形式数组
byte[] num_1_arr= [4,119,38,160,129,59,47,64]
byte[] num_2_arr=[63,98,246,151,31,128,195,64]

#解析8个byte为double
double num1=15.61 
double num2=9984.24

double value = num1+num2 = 10000.0 #原数值


```



# 环境

python3.9, 没有额外依赖

# 附录

## 原dll加密代码

用dnspy打开Monster Train 2\MonsterTrain2_Data\Managed\Assembly-CSharp.dll, 找到了ObfuscatedNumber类, 里面有加密的方式

```c#
namespace ShinyShoe
{
	// Token: 0x02000863 RID: 2147
	[Serializable]
	public class ObfuscatedNumber
	{
		// Token: 0x17000729 RID: 1833
		// (get) Token: 0x06004F27 RID: 20263 RVA: 0x0013FDB2 File Offset: 0x0013DFB2
		// (set) Token: 0x06004F28 RID: 20264 RVA: 0x0013FDD0 File Offset: 0x0013DFD0
		public double Value
		{
			get
			{
				return BitConverter.ToDouble(this._values, 0) + BitConverter.ToDouble(this._values, 8);
			}
			set
			{
double num = new Random().NextDouble() * value; // 随机拆分 value 为两部分
Array.Copy(BitConverter.GetBytes(num), this._values, 8); // 前8字节 = num
Array.Copy(BitConverter.GetBytes(value - num), 0, this._values, 8, 8); // 后8字节 = value - num
			}
		}

		// Token: 0x06004F29 RID: 20265 RVA: 0x0013FE12 File Offset: 0x0013E012
		public ObfuscatedNumber(double initialValue = 0.0)
		{
			this._values = new byte[16];
			this.Value = initialValue;
		}

		// Token: 0x06004F2A RID: 20266 RVA: 0x0013FE30 File Offset: 0x0013E030
		public override string ToString()
		{
			return this.Value.ToString();
		}

		// Token: 0x04002A27 RID: 10791
		[SerializeField]
		private byte[] _values;
	}
}
```



## 一些遗物

```json
    "blessings": [
        {
            "//": "天堂之光1,每层房间+2容量, 薪火+30攻+20血",
            "relicDataID": "9291142a-dc6f-4834-89f1-ceda778e06ec"
        },
        {
            "//": "法术圣所模组(第二层), 战斗开始时, 第二层房间获得法术圣所, 法术-1费",
            "relicDataID": "b037ec04-6164-4cd8-8b9d-3bc420c29351"
        },
        {
            "//": "队长的光环, 回合开始, 所有前排获得2英勇",
            "relicDataID": "19f0d8e3-a3f8-4cac-b73d-46dc189a70ac"
        },
        {
            "//": "破碎光环, 氏族牌只有稀有牌",
            "relicDataID": "8f46fde9-0c75-49ba-9f58-3063864f81bf"
        },
        {
            "//": "受净化的灵魂碎片, 未升级的单位牌费用-1",
            "relicDataID": "f03c7664-0485-4bcf-8bb9-f76321e090c3"
        },
        {
            "//": "但丁的脚凳,部署阶段抽一张房间牌并费用为0",
            "relicDataID": "d245f9d5-e966-4a8e-a125-4aa5b48f1e7c"
        },
        {
            "//": "闪亮臂甲,单位穿戴装备时获得1伤害护盾",
            "relicDataID": "0c50313f-1f07-40c4-8a3e-54748b57981f"
        },
        {
            "//": "泰坦法令, 每层英勇额外提供1护甲",
            "relicDataID": "76511782-d2c1-43d1-9878-e465758017d8"
        },
        {
            "//": "天堂之光2,每层房间+2容量, 薪火+55攻+20血",
            "relicDataID": "2d313e11-aa80-4116-b359-7560d3307544"
        },
        {
            "//": "不稳定的碎片, 友方单位+5攻+12血",
            "relicDataID": "8503360a-26b2-4b71-9334-4c6014ad397f"
        },
        {
            "//": "天堂之息, 后排敌人进入火车时,前进1",
            "relicDataID": "f7b3141b-e803-4128-86cd-d1bf4827d943"
        },
        {
            "//": "残破铁砧, 打出一个法术时, 费用更低的法术本回合免费",
            "relicDataID": "9cc85dbb-d0ae-409b-8f26-41d2202eb1e0"
        },
        {
            "//": "欧迪的图腾, 部署阶段能量-3, 每回合额外获得1能量",
            "relicDataID": "7bc61ac1-f295-4bf5-a978-1c538c8f2e51"
        },
        {
            "//": "薪火石外壳, 单位获得额外升级栏位",
            "relicDataID": "3203c2d3-58f3-4f38-888e-886d8faae758"
        },
        {
            "//": "罪人的药膏, 天灾和祸患牌费用为0",
            "relicDataID": "a19cac7c-b2e0-42bd-bc1e-d180e17a1c15"
        },
        {
            "//": "调和磨石, 部署阶段抽一张装备牌并费用为0",
            "relicDataID": "7a1d5b5d-cd08-4935-b629-d3d441905100"
        },
        {
            "//": "伊莫特之书, 每回合第一张打出的法术获得1个 短暂 复制体",
            "relicDataID": "0f4a9e72-cd34-4667-95f6-6a0ca69832f8"
        },
        {
            "//": "地狱之焰1,每回合+1能量, 部署阶段+1能量, 薪火+30攻+20血",
            "relicDataID": "relicDataID": "780f977e-4007-45ae-900f-c8929b2bf000"
        },
        {
            "//": "地狱之焰2",
            "relicDataID": "6eef1e2d-3bd5-4f04-bd88-d0c24d5eb691"
        },
        {
            "//": "棱彩龙鳞,战斗结束时, 若薪火未受伤害, 则+3龙族宝藏",
            "relicDataID": "26c9bc93-f5a6-439d-8239-14c22cbeb02e"
        },
        {
            "//": "女武神之链, 给天使穿装备, 获得3英勇3再生3狂怒",
            "relicDataID": "c97500a9-b0a4-4c18-b203-b9f4447c84c3"
        },
        {
            "//": "协同镣铐,召唤幼龙时, 所有单位-1冷却",
            "relicDataID": "17ee5d9c-4b87-4250-ad3b-dbe49d118e01"
        },
        {
            "//": "地狱之心,进入薪火室下方楼层的敌方单位受到10薪火溶胶",
            "relicDataID": "e4be072c-e389-4ae7-acc6-0c8aa4cf0078"
        },
        {
            "//": "遗失行李,第一回合抽牌到10张",
            "relicDataID": "2058bafa-a15c-4787-9b9e-4dc7fdf09b74"
        },
        {
            "//": "余烬充能, 第一回合+2能量",
            "relicDataID": "c5a68f6d-671d-4db3-999f-120b5febf41b"
        },
        {
            "//": "会员印记, 商店打折25%",
            "relicDataID": "ffcb6931-e45e-4e27-bacf-4c649779c2be"
        },
        {
            "//": "无常倒影, 奖励的卡牌和单位战旗有随机升级",
            "relicDataID": "9e0e5d4e-6d16-43f1-8cd4-cc4c2b431afd"
        },
        {
            "//": "天界宝石, 友方单位获得英勇时+1层",
            "relicDataID": "74c025fa-ddcb-494b-a790-dcadc5b5772b"
        },
        {
            "//": "火花石催化剂,没有薪火溶胶的敌方单位受到薪火溶胶时, 额外获得6层",
            "relicDataID": "f4c76f11-37d9-4bb5-867a-4d99b7cfa270"
        },
        {
            "//": "菲拉的地狱火, 龙攻击时, 施加5薪火溶胶",
            "relicDataID": "1fdf2fde-a5e7-4eae-86eb-d432145c4621"
        },
        {
            "//": "更大的宝箱, 龙族宝藏容量增加3",
            "relicDataID": "00a8f443-cdea-437a-98bf-0ebe0ead00b0"
        }
    ]
```

