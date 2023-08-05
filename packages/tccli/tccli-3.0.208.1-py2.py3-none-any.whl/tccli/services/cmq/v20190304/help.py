# -*- coding: utf-8 -*-
DESC = "cmq-2019-03-04"
INFO = {
  "CreateTopic": {
    "params": [
      {
        "name": "TopicName",
        "desc": "主题名字，在单个地域同一帐号下唯一。主题名称是一个不超过64个字符的字符串，必须以字母为首字符，剩余部分可以包含字母、数字和横划线（-）。"
      },
      {
        "name": "MaxMsgSize",
        "desc": "消息最大长度。取值范围 1024-65536 Byte（即1-64K），默认值 65536。"
      },
      {
        "name": "FilterType",
        "desc": "用于指定主题的消息匹配策略。1：表示标签匹配策略；2：表示路由匹配策略，默认值为标签匹配策略。"
      },
      {
        "name": "MsgRetentionSeconds",
        "desc": "消息保存时间。取值范围60 - 86400 s（即1分钟 - 1天），默认值86400。"
      },
      {
        "name": "Trace",
        "desc": "是否开启消息轨迹标识，true表示开启，false表示不开启，不填表示不开启。"
      }
    ],
    "desc": "创建主题"
  },
  "CreateSubscribe": {
    "params": [
      {
        "name": "TopicName",
        "desc": "主题名字，在单个地域同一帐号下唯一。主题名称是一个不超过64个字符的字符串，必须以字母为首字符，剩余部分可以包含字母、数字和横划线（-）。"
      },
      {
        "name": "SubscriptionName",
        "desc": "订阅名字，在单个地域同一帐号的同一主题下唯一。订阅名称是一个不超过64个字符的字符串，必须以字母为首字符，剩余部分可以包含字母、数字和横划线(-)。"
      },
      {
        "name": "Protocol",
        "desc": "订阅的协议，目前支持两种协议：http、queue。使用http协议，用户需自己搭建接受消息的web server。使用queue，消息会自动推送到CMQ queue，用户可以并发地拉取消息。"
      },
      {
        "name": "Endpoint",
        "desc": "接收通知的Endpoint，根据协议Protocol区分：对于http，Endpoint必须以“`http://`”开头，host可以是域名或IP；对于Queue，则填QueueName。 请注意，目前推送服务不能推送到私有网络中，因此Endpoint填写为私有网络域名或地址将接收不到推送的消息，目前支持推送到公网和基础网络。"
      },
      {
        "name": "NotifyStrategy",
        "desc": "向Endpoint推送消息出现错误时，CMQ推送服务器的重试策略。取值有：1）BACKOFF_RETRY，退避重试。每隔一定时间重试一次，重试够一定次数后，就把该消息丢弃，继续推送下一条消息；2）EXPONENTIAL_DECAY_RETRY，指数衰退重试。每次重试的间隔是指数递增的，例如开始1s，后面是2s，4s，8s...由于Topic消息的周期是一天，所以最多重试一天就把消息丢弃。默认值是EXPONENTIAL_DECAY_RETRY。"
      },
      {
        "name": "FilterTag",
        "desc": "消息正文。消息标签（用于消息过滤)。标签数量不能超过5个，每个标签不超过16个字符。与(Batch)PublishMessage的MsgTag参数配合使用，规则：1）如果FilterTag没有设置，则无论MsgTag是否有设置，订阅接收所有发布到Topic的消息；2）如果FilterTag数组有值，则只有数组中至少有一个值在MsgTag数组中也存在时（即FilterTag和MsgTag有交集），订阅才接收该发布到Topic的消息；3）如果FilterTag数组有值，但MsgTag没设置，则不接收任何发布到Topic的消息，可以认为是2）的一种特例，此时FilterTag和MsgTag没有交集。规则整体的设计思想是以订阅者的意愿为主。"
      },
      {
        "name": "BindingKey",
        "desc": "BindingKey数量不超过5个， 每个BindingKey长度不超过64字节，该字段表示订阅接收消息的过滤策略，每个BindingKey最多含有15个“.”， 即最多16个词组。"
      },
      {
        "name": "NotifyContentFormat",
        "desc": "推送内容的格式。取值：1）JSON；2）SIMPLIFIED，即raw格式。如果Protocol是queue，则取值必须为SIMPLIFIED。如果Protocol是http，两个值均可以，默认值是JSON。"
      }
    ],
    "desc": "创建订阅接口"
  },
  "ModifyTopicAttribute": {
    "params": [
      {
        "name": "TopicName",
        "desc": "主题名字，在单个地域同一帐号下唯一。主题名称是一个不超过64个字符的字符串，必须以字母为首字符，剩余部分可以包含字母、数字和横划线(-)。"
      },
      {
        "name": "MaxMsgSize",
        "desc": "消息最大长度。取值范围1024 - 65536 Byte（即1 - 64K），默认值65536。"
      },
      {
        "name": "MsgRetentionSeconds",
        "desc": "消息保存时间。取值范围60 - 86400 s（即1分钟 - 1天），默认值86400。"
      },
      {
        "name": "Trace",
        "desc": "是否开启消息轨迹标识，true表示开启，false表示不开启，不填表示不开启。"
      }
    ],
    "desc": "修改主题属性"
  },
  "ClearSubscriptionFilterTags": {
    "params": [
      {
        "name": "TopicName",
        "desc": "主题名字，在单个地域同一帐号下唯一。主题名称是一个不超过64个字符的字符串，必须以字母为首字符，剩余部分可以包含字母、数字和横划线（-）。"
      },
      {
        "name": "SubscriptionName",
        "desc": "订阅名字，在单个地域同一帐号的同一主题下唯一。订阅名称是一个不超过64个字符的字符串，必须以字母为首字符，剩余部分可以包含字母、数字和横划线(-)。"
      }
    ],
    "desc": "清空订阅者消息标签"
  },
  "DeleteSubscribe": {
    "params": [
      {
        "name": "TopicName",
        "desc": "主题名字，在单个地域同一帐号下唯一。主题名称是一个不超过64个字符的字符串，必须以字母为首字符，剩余部分可以包含字母、数字和横划线(-)。"
      },
      {
        "name": "SubscriptionName",
        "desc": "订阅名字，在单个地域同一帐号的同一主题下唯一。订阅名称是一个不超过64个字符的字符串，必须以字母为首字符，剩余部分可以包含字母、数字和横划线(-)。"
      }
    ],
    "desc": "删除订阅"
  },
  "CreateQueue": {
    "params": [
      {
        "name": "QueueName",
        "desc": "队列名字，在单个地域同一帐号下唯一。队列名称是一个不超过 64 个字符的字符串，必须以字母为首字符，剩余部分可以包含字母、数字和横划线(-)。"
      },
      {
        "name": "MaxMsgHeapNum",
        "desc": "最大堆积消息数。取值范围在公测期间为 1,000,000 - 10,000,000，正式上线后范围可达到 1000,000-1000,000,000。默认取值在公测期间为 10,000,000，正式上线后为 100,000,000。"
      },
      {
        "name": "PollingWaitSeconds",
        "desc": "消息接收长轮询等待时间。取值范围 0-30 秒，默认值 0。"
      },
      {
        "name": "VisibilityTimeout",
        "desc": "消息可见性超时。取值范围 1-43200 秒（即12小时内），默认值 30。"
      },
      {
        "name": "MaxMsgSize",
        "desc": "消息最大长度。取值范围 1024-65536 Byte（即1-64K），默认值 65536。"
      },
      {
        "name": "MsgRetentionSeconds",
        "desc": "消息保留周期。取值范围 60-1296000 秒（1min-15天），默认值 345600 (4 天)。"
      },
      {
        "name": "RewindSeconds",
        "desc": "队列是否开启回溯消息能力，该参数取值范围0-msgRetentionSeconds,即最大的回溯时间为消息在队列中的保留周期，0表示不开启。"
      },
      {
        "name": "Transaction",
        "desc": "1 表示事务队列，0 表示普通队列"
      },
      {
        "name": "FirstQueryInterval",
        "desc": "第一次回查间隔"
      },
      {
        "name": "MaxQueryCount",
        "desc": "最大回查次数"
      },
      {
        "name": "DeadLetterQueueName",
        "desc": "死信队列名称"
      },
      {
        "name": "Policy",
        "desc": "死信策略。0为消息被多次消费未删除，1为Time-To-Live过期"
      },
      {
        "name": "MaxReceiveCount",
        "desc": "最大接收次数 1-1000"
      },
      {
        "name": "MaxTimeToLive",
        "desc": "policy为1时必选。最大未消费过期时间。范围300-43200，单位秒，需要小于消息最大保留时间msgRetentionSeconds"
      },
      {
        "name": "Trace",
        "desc": "是否开启消息轨迹追踪，当不设置字段时，默认为不开启，该字段为true表示开启，为false表示不开启"
      }
    ],
    "desc": "创建队列接口\n"
  },
  "RewindQueue": {
    "params": [
      {
        "name": "QueueName",
        "desc": "队列名字，在单个地域同一帐号下唯一。队列名称是一个不超过64个字符的字符串，必须以字母为首字符，剩余部分可以包含字母、数字和横划线(-)。"
      },
      {
        "name": "StartConsumeTime",
        "desc": "设定该时间，则（Batch）receiveMessage接口，会按照生产消息的先后顺序消费该时间戳以后的消息。"
      }
    ],
    "desc": "回溯队列"
  },
  "ModifySubscriptionAttribute": {
    "params": [
      {
        "name": "TopicName",
        "desc": "主题名字，在单个地域同一帐号下唯一。主题名称是一个不超过64个字符的字符串，必须以字母为首字符，剩余部分可以包含字母、数字和横划线（-）。"
      },
      {
        "name": "SubscriptionName",
        "desc": "订阅名字，在单个地域同一帐号的同一主题下唯一。订阅名称是一个不超过64个字符的字符串，必须以字母为首字符，剩余部分可以包含字母、数字和横划线(-)。"
      },
      {
        "name": "NotifyStrategy",
        "desc": "向 Endpoint 推送消息出现错误时，CMQ 推送服务器的重试策略。取值如下：\n（1）BACKOFF_RETRY，退避重试。每隔一定时间重试一次，重试够一定次数后，就把该消息丢弃，继续推送下一条消息。\n（2）EXPONENTIAL_DECAY_RETRY，指数衰退重试。每次重试的间隔是指数递增的，例如开始1s，后面是2s，4s，8s···由于 Topic 消息的周期是一天，所以最多重试一天就把消息丢弃。默认值是 EXPONENTIAL_DECAY_RETRY。"
      },
      {
        "name": "NotifyContentFormat",
        "desc": "推送内容的格式。取值：（1）JSON；（2）SIMPLIFIED，即 raw 格式。如果 Protocol 是 queue，则取值必须为 SIMPLIFIED。如果 Protocol 是 HTTP，两个值均可以，默认值是 JSON。"
      },
      {
        "name": "FilterTags",
        "desc": "消息正文。消息标签（用于消息过滤)。标签数量不能超过5个，每个标签不超过16个字符。与(Batch)PublishMessage的MsgTag参数配合使用，规则：1）如果FilterTag没有设置，则无论MsgTag是否有设置，订阅接收所有发布到Topic的消息；2）如果FilterTag数组有值，则只有数组中至少有一个值在MsgTag数组中也存在时（即FilterTag和MsgTag有交集），订阅才接收该发布到Topic的消息；3）如果FilterTag数组有值，但MsgTag没设置，则不接收任何发布到Topic的消息，可以认为是2）的一种特例，此时FilterTag和MsgTag没有交集。规则整体的设计思想是以订阅者的意愿为主。"
      },
      {
        "name": "BindingKey",
        "desc": "BindingKey数量不超过5个， 每个BindingKey长度不超过64字节，该字段表示订阅接收消息的过滤策略，每个BindingKey最多含有15个“.”， 即最多16个词组。"
      }
    ],
    "desc": "修改订阅属性"
  },
  "DescribeQueueDetail": {
    "params": [
      {
        "name": "Offset",
        "desc": "分页时本页获取队列列表的起始位置。如果填写了该值，必须也要填写 limit 。该值缺省时，后台取默认值 0"
      },
      {
        "name": "Limit",
        "desc": "分页时本页获取队列的个数，如果不传递该参数，则该参数默认为20，最大值为50。"
      },
      {
        "name": "Filters",
        "desc": "筛选参数，目前支持QueueName筛选，且仅支持一个关键字"
      },
      {
        "name": "TagKey",
        "desc": "标签搜索"
      },
      {
        "name": "QueueName",
        "desc": "精确匹配QueueName"
      }
    ],
    "desc": "枚举队列"
  },
  "DeleteQueue": {
    "params": [
      {
        "name": "QueueName",
        "desc": "队列名字，在单个地域同一帐号下唯一。队列名称是一个不超过64个字符的字符串，必须以字母为首字符，剩余部分可以包含字母、数字和横划线(-)。"
      }
    ],
    "desc": "DeleteQueue"
  },
  "UnbindDeadLetter": {
    "params": [
      {
        "name": "QueueName",
        "desc": "死信策略源队列名称，调用本接口会清空该队列的死信队列策略。"
      }
    ],
    "desc": "解绑死信队列"
  },
  "DeleteTopic": {
    "params": [
      {
        "name": "TopicName",
        "desc": "主题名字，在单个地域同一帐号下唯一。主题名称是一个不超过64个字符的字符串，必须以字母为首字符，剩余部分可以包含字母、数字和横划线(-)。"
      }
    ],
    "desc": "删除主题"
  },
  "DescribeTopicDetail": {
    "params": [
      {
        "name": "Offset",
        "desc": "分页时本页获取队列列表的起始位置。如果填写了该值，必须也要填写 limit 。该值缺省时，后台取默认值 0。"
      },
      {
        "name": "Limit",
        "desc": "分页时本页获取队列的个数，如果不传递该参数，则该参数默认为20，最大值为50。"
      },
      {
        "name": "Filters",
        "desc": "目前只支持过滤TopicName ， 且只能填一个过滤值。"
      },
      {
        "name": "TagKey",
        "desc": "标签匹配。"
      },
      {
        "name": "TopicName",
        "desc": "精确匹配TopicName。"
      }
    ],
    "desc": "查询主题详情 "
  },
  "DescribeSubscriptionDetail": {
    "params": [
      {
        "name": "TopicName",
        "desc": "主题名字，在单个地域同一帐号下唯一。主题名称是一个不超过64个字符的字符串，必须以字母为首字符，剩余部分可以包含字母、数字和横划线（-）。"
      },
      {
        "name": "Offset",
        "desc": "分页时本页获取主题列表的起始位置。如果填写了该值，必须也要填写 limit 。该值缺省时，后台取默认值 0"
      },
      {
        "name": "Limit",
        "desc": "分页时本页获取主题的个数，如果不传递该参数，则该参数默认为20，最大值为50。"
      },
      {
        "name": "Filters",
        "desc": "筛选参数，目前只支持SubscriptionName，且仅支持一个关键字。"
      }
    ],
    "desc": "查询订阅详情"
  },
  "DescribeDeadLetterSourceQueues": {
    "params": [
      {
        "name": "DeadLetterQueueName",
        "desc": "死信队列名称"
      },
      {
        "name": "Limit",
        "desc": "分页时本页获取主题列表的起始位置。如果填写了该值，必须也要填写 limit 。该值缺省时，后台取默认值 0。"
      },
      {
        "name": "Offset",
        "desc": "分页时本页获取主题的个数，如果不传递该参数，则该参数默认为20，最大值为50。"
      },
      {
        "name": "Filters",
        "desc": "过滤死信队列源队列名称，目前仅支持SourceQueueName过滤"
      }
    ],
    "desc": "枚举死信队列源队列"
  },
  "ClearQueue": {
    "params": [
      {
        "name": "QueueName",
        "desc": "队列名字，在单个地域同一帐号下唯一。队列名称是一个不超过64个字符的字符串，必须以字母为首字符，剩余部分可以包含字母、数字和横划线(-)。"
      }
    ],
    "desc": "清除queue中的所有消息"
  },
  "ModifyQueueAttribute": {
    "params": [
      {
        "name": "QueueName",
        "desc": "队列名字，在单个地域同一帐号下唯一。队列名称是一个不超过 64 个字符的字符串，必须以字母为首字符，剩余部分可以包含字母、数字和横划线(-)。"
      },
      {
        "name": "MaxMsgHeapNum",
        "desc": "最大堆积消息数。取值范围在公测期间为 1,000,000 - 10,000,000，正式上线后范围可达到 1000,000-1000,000,000。默认取值在公测期间为 10,000,000，正式上线后为 100,000,000。"
      },
      {
        "name": "PollingWaitSeconds",
        "desc": "消息接收长轮询等待时间。取值范围 0-30 秒，默认值 0。"
      },
      {
        "name": "VisibilityTimeout",
        "desc": "消息可见性超时。取值范围 1-43200 秒（即12小时内），默认值 30。"
      },
      {
        "name": "MaxMsgSize",
        "desc": "消息最大长度。取值范围 1024-65536 Byte（即1-64K），默认值 65536。"
      },
      {
        "name": "MsgRetentionSeconds",
        "desc": "消息保留周期。取值范围 60-1296000 秒（1min-15天），默认值 345600 (4 天)。"
      },
      {
        "name": "RewindSeconds",
        "desc": "消息最长回溯时间，取值范围0-msgRetentionSeconds，消息的最大回溯之间为消息在队列中的保存周期，0表示不开启消息回溯。"
      },
      {
        "name": "FirstQueryInterval",
        "desc": "第一次查询时间"
      },
      {
        "name": "MaxQueryCount",
        "desc": "最大查询次数"
      },
      {
        "name": "DeadLetterQueueName",
        "desc": "死信队列名称"
      },
      {
        "name": "MaxTimeToLive",
        "desc": "MaxTimeToLivepolicy为1时必选。最大未消费过期时间。范围300-43200，单位秒，需要小于消息最大保留时间MsgRetentionSeconds"
      },
      {
        "name": "MaxReceiveCount",
        "desc": "最大接收次数"
      },
      {
        "name": "Policy",
        "desc": "死信队列策略"
      },
      {
        "name": "Trace",
        "desc": "是否开启消息轨迹标识，true表示开启，false表示不开启，不填表示不开启。"
      }
    ],
    "desc": "修改队列属性"
  }
}