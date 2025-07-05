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

