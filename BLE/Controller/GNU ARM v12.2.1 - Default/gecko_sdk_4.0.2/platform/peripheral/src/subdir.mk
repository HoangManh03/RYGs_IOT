################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
D:/SDK/gecko_sdk-gsdk_4.0/platform/peripheral/src/peripheral_sysrtc.c 

OBJS += \
./gecko_sdk_4.0.2/platform/peripheral/src/peripheral_sysrtc.o 

C_DEPS += \
./gecko_sdk_4.0.2/platform/peripheral/src/peripheral_sysrtc.d 


# Each subdirectory must supply rules for building sources it contributes
gecko_sdk_4.0.2/platform/peripheral/src/peripheral_sysrtc.o: D:/SDK/gecko_sdk-gsdk_4.0/platform/peripheral/src/peripheral_sysrtc.c gecko_sdk_4.0.2/platform/peripheral/src/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: GNU ARM C Compiler'
	arm-none-eabi-gcc -g -gdwarf-2 -mcpu=cortex-m33 -mthumb -std=c99 '-DEFR32MG24B310F1536IM48=1' '-DSL_BOARD_NAME="BRD2601B"' '-DSL_BOARD_REV="A01"' '-DSL_COMPONENT_CATALOG_PRESENT=1' '-DMBEDTLS_CONFIG_FILE=<mbedtls_config.h>' '-DMBEDTLS_PSA_CRYPTO_CONFIG_FILE=<psa_crypto_config.h>' '-DSL_RAIL_LIB_MULTIPROTOCOL_SUPPORT=0' '-DSL_RAIL_UTIL_PA_CONFIG_HEADER=<sl_rail_util_pa_config.h>' '-DSLI_RADIOAES_REQUIRES_MASKING=1' -I"D:\IOT2024\RYGs_IOT\BLE\Controller\autogen" -I"D:\IOT2024\RYGs_IOT\BLE\Controller\config" -I"D:\IOT2024\RYGs_IOT\BLE\Controller\config\btconf" -I"D:\IOT2024\RYGs_IOT\BLE\Controller" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/Device/SiliconLabs/EFR32MG24/Include" -I"D:/SDK/gecko_sdk-gsdk_4.0//app/common/util/app_assert" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/common/inc" -I"D:/SDK/gecko_sdk-gsdk_4.0//protocol/bluetooth/inc" -I"D:/SDK/gecko_sdk-gsdk_4.0//hardware/board/inc" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/bootloader" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/bootloader/api" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/driver/button/inc" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/CMSIS/Include" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/service/device_init/inc" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/emdrv/common/inc" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/emlib/inc" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/emlib/host/inc" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/emdrv/gpiointerrupt/inc" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/service/hfxo_manager/inc" -I"D:/SDK/gecko_sdk-gsdk_4.0//util/third_party/crypto/sl_component/sl_mbedtls_support/config" -I"D:/SDK/gecko_sdk-gsdk_4.0//util/third_party/crypto/mbedtls/include" -I"D:/SDK/gecko_sdk-gsdk_4.0//util/third_party/crypto/mbedtls/library" -I"D:/SDK/gecko_sdk-gsdk_4.0//util/third_party/crypto/sl_component/sl_mbedtls_support/inc" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/service/mpu/inc" -I"D:/SDK/gecko_sdk-gsdk_4.0//hardware/driver/mx25_flash_shutdown/inc/sl_mx25_flash_shutdown_eusart" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/emdrv/nvm3/inc" -I"D:/SDK/gecko_sdk-gsdk_4.0//app/bluetooth/common/ota_dfu" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/peripheral/inc" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/service/power_manager/inc" -I"D:/SDK/gecko_sdk-gsdk_4.0//util/third_party/crypto/sl_component/sl_psa_driver/inc" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/radio/rail_lib/common" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/radio/rail_lib/protocol/ble" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/radio/rail_lib/protocol/ieee802154" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/radio/rail_lib/protocol/zwave" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/radio/rail_lib/chip/efr32/efr32xg2x" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/radio/rail_lib/plugin/pa-conversions" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/radio/rail_lib/plugin/pa-conversions/efr32xg24" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/radio/rail_lib/plugin/rail_util_pti" -I"D:/SDK/gecko_sdk-gsdk_4.0//util/third_party/crypto/sl_component/se_manager/inc" -I"D:/SDK/gecko_sdk-gsdk_4.0//util/third_party/crypto/sl_component/se_manager/src" -I"D:/SDK/gecko_sdk-gsdk_4.0//util/silicon_labs/silabs_core/memory_manager" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/common/toolchain/inc" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/service/system/inc" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/service/sleeptimer/inc" -I"D:/SDK/gecko_sdk-gsdk_4.0//util/third_party/crypto/sl_component/sl_protocol_crypto/src" -I"D:/SDK/gecko_sdk-gsdk_4.0//platform/service/udelay/inc" -Os -Wall -Wextra -fno-builtin -ffunction-sections -fdata-sections -imacrossl_gcc_preinclude.h -mfpu=fpv5-sp-d16 -mfloat-abi=hard -c -fmessage-length=0 -MMD -MP -MF"gecko_sdk_4.0.2/platform/peripheral/src/peripheral_sysrtc.d" -MT"$@" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


