#include <android/hardware/boot/1.2/IBootControl.h>
#include <android/hardware/boot/1.2/types.h>

using ::android::hardware::boot::V1_2::IBootControl;
using ::android::hardware::boot::V1_2::Slot;
using ::android::hardware::boot::V1_2::BoolResult;

class BootControl : public IBootControl {
};
