kungfu::event_ptr参数详解
===============================

kungfu共享内存结构
------------------------



kungfu框架中进程间通信采用共享内存队列的形式, 一个进程将数据写入共享内存文件, 其他多个进程可以同时读取.

一条信道对应一个逻辑上的journal文件, 表示逻辑上一个无限大的队列.

具体实现时将一个journal切分为多个固定大小的page, 只要磁盘足够大就可以无限的增加page的个数, 每一个page文件的命名规则为 **"dest_id的十六进制进程.page数.journal"**.

存放在写入进程的目录下, 实盘模式下写入进程的journal所属目录命名规则为 **"$KF_HOME/runtime/journal/{category}/{group}/{name}/{mode}"**.

范例

.. code-block:: shell
    :linenos: 

    $KF_HOME/runtime/journal/td/CTP/089270/live, 表示实盘模式的CTP柜台对应账户为089270的共享内存文件目录    


每一个page存放具体的数据, 每一个数据视为一个frame, frame由frame_header和data组成.

journal的结构如下图所示, 

.. image:: broker/_images/journal.png


------------------------


kungfu::event_ptr
----------------------

在kungfu系统中, 所有的"typename_ptr"都实际表示std::shared_ptr<typename>, 
即kungfu::event_ptr表示std::shared_ptr<kungfu::event>.

当A进程往共享内存里写入一个数据时, 会生成一个frame, 里面包含了frame_header和具体的数据内容, 
当B进程读到该数据时, 也会将frame_header和后面的数据封装成一个frame, kungfu::event_ptr就是指向这个frame的指针, 
B进程会根据frame_header里面的数据类型msg_type触发不同的函数.

例如当策略调用下单时, 会往共享内存里写入一个OrderInput数据, TD读取到这个数据时, 会把frame_header和OrderInput封装在一个frame里, 
然后调用虚函数insert_order函数, 并且把指向这个frame的指针kungfu::event_ptr作为参数传入,
在override的insert_order函数里通过调用event的对应函数, 可以获取到这个frame里面的frame_header和具体数据OrderInput的信息.


范例

.. code-block:: cpp
    :linenos: 

    //ctp的insert_order实现
    bool TraderCTP::insert_order(const event_ptr &event) {
        const OrderInput &input = event->data<OrderInput>();
        SPDLOG_DEBUG("OrderInput: {}", input.to_string());

        int request_id = get_request_id();
        int error_id = 0;
        uint64_t orderRef_key = 0;

        CThostFtdcInputOrderField ctp_input{};
        to_ctp(ctp_input, input);
        strcpy(ctp_input.BrokerID, config_.broker_id.c_str());
        strcpy(ctp_input.InvestorID, config_.account_id.c_str());
        strcpy(ctp_input.OrderRef, std::to_string(++order_ref_).c_str());
        SPDLOG_DEBUG("CThostFtdcInputOrderField: {}", to_string(ctp_input));
        error_id = api_->ReqOrderInsert(&ctp_input, request_id);
        orderRef_key = get_orderRef_key(front_id_, session_id_, ctp_input.OrderRef);

        auto nano = time::now_in_nano();
        auto writer = get_writer(event->source());
        Order &order = writer->open_data<Order>(event->gen_time());
        order_from_input(input, order);
        order.insert_time = nano;
        order.update_time = nano;
        order.time_condition = from_ctp_time_condition(ctp_input.TimeCondition);

        if (error_id != 0) {
            order.error_id = error_id;
            order.status = OrderStatus::Error;
        }

        SPDLOG_DEBUG("Order: {}", order.to_string());
        writer->close_data();
        map_request_id_to_kf_order_id_.insert_or_assign(request_id, uint64_t(input.order_id));
        map_OrderRefKey_to_kf_order_id_.insert_or_assign(orderRef_key, uint64_t(input.order_id));
        map_kf_order_id_to_OrderRef_.insert_or_assign(input.order_id, ctp_input.OrderRef);
        return error_id == 0;
    }


------------------------------------    



.. frame_header, event和frame的定义如下:

.. .. code-block:: cpp
..     :linenos:    

..     // frame_header的数据结构
..     KF_DEFINE_PACK_TYPE(                                           //
..         frame_header, 0, PK(gen_time), TIMESTAMP(gen_time),        //
..         /** total frame length (including header and data body) */ //
..         (volatile uint32_t, length),                               //
..         /** header length */                                       //
..         (uint32_t, header_length),                                 //
..         /** generate time of the frame data */                     //
..         (int64_t, gen_time),                                       //
..         /** trigger time for this frame, use for latency stats */  //
..         (int64_t, trigger_time),                                   //
..         /** msg type of the data in frame */                       //
..         (volatile int32_t, msg_type),                              //
..         /** source of this frame */                                //
..         (uint32_t, source),                                        //
..         /** dest of this frame */                                  //
..         (uint32_t, dest),                                          //
..         /** json or raw struct */                                  //
..         (enums::FrameDataType, data_type),                         //
..         /** the real writer of this frame */                       //
..         (uint32_t, initial_source),                                //
..         /** key of frame */                                        //
..         (uint64_t, frame_uid),                                     //
..         /** current_frame of reader when generate this frame */    //
..         (uint64_t, trigger_frame_uid)                              //
..     );

..     struct event {
..         virtual ~event() = default;

..         [[nodiscard]] virtual int64_t gen_time() const = 0;         

..         [[nodiscard]] virtual int64_t trigger_time() const = 0;     

..         [[nodiscard]] virtual int32_t msg_type() const = 0;         

..         [[nodiscard]] virtual uint32_t source() const = 0;          

..         [[nodiscard]] virtual uint32_t initial_source() const = 0;  

..         [[nodiscard]] virtual uint32_t dest() const = 0;            

..         [[nodiscard]] virtual uint32_t data_length() const = 0;     

..         [[nodiscard]] virtual const void *data_address() const = 0; 

..         [[nodiscard]] virtual const char *data_as_bytes() const = 0; 

..         [[nodiscard]] virtual std::vector<uint8_t> data_as_byte_array() const = 0; 

..         [[nodiscard]] virtual std::string data_as_string() const = 0; 

..         [[nodiscard]] virtual std::string to_string() const = 0;      

..         [[nodiscard]] virtual int8_t data_type() const = 0;

..         [[nodiscard]] virtual bool is_json() const = 0;

..         [[nodiscard]] virtual uint64_t frame_uid() const = 0;

..         [[nodiscard]] virtual uint64_t trigger_frame_uid() const = 0;

..         /**
..         * Using auto with the return mess up the reference with the undlerying memory address, DO NOT USE it.
..         * @tparam T
..         * @return a casted reference to the underlying memory address
..         */
..         template <typename T> std::enable_if_t<size_fixed_v<T> or std::is_same_v<T, nlohmann::json>, const T &> data() const {
..             return *(reinterpret_cast<const T *>(data_address()));
..         }

..         template <typename T>
..         std::enable_if_t<not size_fixed_v<T> and not std::is_same_v<T, nlohmann::json>, const T> data() const {
..             return T(data_as_bytes(), data_length());
..         }

..         template <class T> const T &custom_data() const { return *(reinterpret_cast<const T *>(data_address())); }
..     };

..     struct frame : event {
..         ~frame() override = default;

..         [[nodiscard]] bool has_data() const { return header_->length > 0 && header_->msg_type > 0; }

..         [[nodiscard]] uintptr_t address() const { return reinterpret_cast<uintptr_t>(header_); }

..         [[nodiscard]] uint32_t frame_length() const { return header_->length; }

..         [[nodiscard]] uint32_t header_length() const { return header_->header_length; }

..         [[nodiscard]] uint32_t data_length() const override { return frame_length() - header_length(); }

..         [[nodiscard]] int64_t gen_time() const override { return header_->gen_time; }

..         [[nodiscard]] int64_t trigger_time() const override { return header_->trigger_time; }

..         [[nodiscard]] int32_t msg_type() const override { return header_->msg_type; }

..         [[nodiscard]] uint32_t source() const override { return header_->source; }

..         [[nodiscard]] uint32_t initial_source() const override { return header_->initial_source; }

..         [[nodiscard]] uint32_t dest() const override { return header_->dest; }

..         [[nodiscard]] const void *data_address() const override {
..             return reinterpret_cast<void *>(address() + header_length());
..         }

..         [[nodiscard]] const char *data_as_bytes() const override {
..             return reinterpret_cast<char *>(address() + header_length());
..         }

..         [[nodiscard]] std::vector<uint8_t> data_as_byte_array() const override {
..             return {data_as_bytes(), data_as_bytes() + data_length()};
..         }

..         [[nodiscard]] std::string data_as_string() const override { return std::string{data_as_bytes(), data_length()}; }

..         [[nodiscard]] std::string to_string() const override {
..             auto j = header_->to_json();
..             j["data"] = data_as_string();
..             return j.dump(-1, ' ', false, nlohmann::json::basic_json::error_handler_t::replace);
..         }

..         [[nodiscard]] int8_t data_type() const override { return int8_t(header_->data_type); }

..         [[nodiscard]] bool is_json() const override { return data_type() == longfist::enums::FrameDataType::Json; }

..         [[nodiscard]] uint64_t frame_uid() const override { return header_->frame_uid; }

..         [[nodiscard]] uint64_t trigger_frame_uid() const override { return header_->trigger_frame_uid; }

..         template <typename T> size_t copy_data(const T &data) {
..             size_t length = sizeof(T);
..             memcpy(const_cast<void *>(data_address()), &data, length);
..             return length;
..         }

..         private:
..         longfist::types::frame_header *header_ = nullptr;

..         frame() = default;

..         void set_address(uintptr_t address) { header_ = reinterpret_cast<longfist::types::frame_header *>(address); }

..         void move_to_next() { set_address(address() + frame_length()); }

..         void set_header_length() { header_->header_length = sizeof(longfist::types::frame_header); }

..         void set_data_length(uint32_t length) { header_->length = header_length() + length; }

..         void set_gen_time(int64_t gen_time) { header_->gen_time = gen_time; }

..         void set_trigger_time(int64_t trigger_time) { header_->trigger_time = trigger_time; }

..         void set_msg_type(int32_t msg_type) { header_->msg_type = msg_type; }

..         void set_data_type(longfist::enums::FrameDataType data_type) { header_->data_type = data_type; }

..         void set_source(uint32_t source) { header_->source = source; }

..         void set_initial_source(uint32_t initial_source) { header_->initial_source = initial_source; }

..         void set_dest(uint32_t dest) { header_->dest = dest; }

..         void set_frame_uid(uint64_t frame_uid) { header_->frame_uid = frame_uid; }

..         void set_trigger_frame_uid(uint64_t trigger_frame_uid) { header_->trigger_frame_uid = trigger_frame_uid; }

..         void copy(const frame &source) { memcpy(header_, source.header_, source.frame_length()); }

..         friend struct cloned_frame;

..         friend class journal;

..         friend class writer;

..         friend class replay_writer;
..     };

    


.. ------------------------