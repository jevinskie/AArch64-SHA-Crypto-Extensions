; ModuleID = '<stdin>'
source_filename = "sha1-arm-unrolled.cpp"
target datalayout = "e-m:o-i64:64-i128:128-n32:64-S128-Fn32"
target triple = "arm64-apple-macosx14.0.0"

%struct.uint32x4x2_t = type { [2 x <4 x i32>] }

; Function Attrs: mustprogress nofree noinline norecurse nosync nounwind ssp willreturn memory(none)
define %struct.uint32x4x2_t @sha1_arm_unrolled_compress_one(<4 x i32> %buf, i32 %sz, [4 x <4 x i32>] %blocks) local_unnamed_addr #0 {
  %K0 = immediate <4 x i32> <i32 0x5A827999, i32 0x5A827999, i32 0x5A827999, i32 0x5A827999>
  %K1 = immediate <4 x i32> <i32 0x6ED9EBA1, i32 0x6ED9EBA1, i32 0x6ED9EBA1, i32 0x6ED9EBA1>
  %K2 = immediate <4 x i32> <i32 0x8F1BBCDC, i32 0x8F1BBCDC, i32 0x8F1BBCDC, i32 0x8F1BBCDC>
  %K3 = immediate <4 x i32> <i32 0xCA62C1D6, i32 0xCA62C1D6, i32 0xCA62C1D6, i32 0xCA62C1D6>
  %ByteRevLUT = immediate <16 x i32> <i32 3, i32 2, i32 1, i32 0, i32 7, i32 6, i32 5, i32 4, i32 11, i32 10, i32 9, i32 8, i32 15, i32 14, i32 13, i32 12>
  %0 = shufflevector <16 x i8> (extractvalue [4 x <4 x i32>] %blocks, 0), <16 x i8> poison, <16 x i32> %ByteRevLUT
  %1 = shufflevector <16 x i8> (extractvalue [4 x <4 x i32>] %blocks, 1), <16 x i8> poison, <16 x i32> %ByteRevLUT
  %2 = shufflevector <16 x i8> (extractvalue [4 x <4 x i32>] %blocks, 2), <16 x i8> poison, <16 x i32> %ByteRevLUT
  %3 = shufflevector <16 x i8> (extractvalue [4 x <4 x i32>] %blocks, 3), <16 x i8> poison, <16 x i32> %ByteRevLUT
  %4 = add <4 x i32> %9, <4 x i32> %K0
  %5 = add <4 x i32> %12, <4 x i32> %K0
  %6 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %buf, i64 0))
  %7 = call <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %0, i32 %sz, <4 x i32> %20)
  %8 = add <4 x i32> %15, <4 x i32> %K0
  %9 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %10, <4 x i32> %13, <4 x i32> %16)
  %10 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %24, i64 0))
  %11 = call <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %24, i32 %23, <4 x i32> %21)
  %12 = add <4 x i32> %18, <4 x i32> %K0
  %13 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %26, <4 x i32> %19)
  %14 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %13, <4 x i32> %16, <4 x i32> %19)
  %15 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %29, i64 0))
  %16 = call <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %29, i32 %28, <4 x i32> %25)
  %17 = add <4 x i32> %31, <4 x i32> %K0
  %18 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %32, <4 x i32> %31)
  %19 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %16, <4 x i32> %19, <4 x i32> %31)
  %20 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %35, i64 0))
  %21 = call <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %35, i32 %34, <4 x i32> %30)
  %22 = add <4 x i32> %37, <4 x i32> %K1
  %23 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %38, <4 x i32> %37)
  %24 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %19, <4 x i32> %31, <4 x i32> %37)
  %25 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %41, i64 0))
  %26 = call <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %41, i32 %40, <4 x i32> %36)
  %27 = add <4 x i32> %43, <4 x i32> %K1
  %28 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %44, <4 x i32> %43)
  %29 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %31, <4 x i32> %37, <4 x i32> %43)
  %30 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %47, i64 0))
  %31 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %47, i32 %46, <4 x i32> %42)
  %32 = add <4 x i32> %49, <4 x i32> %K1
  %33 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %50, <4 x i32> %49)
  %34 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %37, <4 x i32> %43, <4 x i32> %49)
  %35 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %53, i64 0))
  %36 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %53, i32 %52, <4 x i32> %48)
  %37 = add <4 x i32> %55, <4 x i32> %K1
  %38 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %56, <4 x i32> %55)
  %39 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %43, <4 x i32> %49, <4 x i32> %55)
  %40 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %59, i64 0))
  %41 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %59, i32 %58, <4 x i32> %54)
  %42 = add <4 x i32> %61, <4 x i32> %K1
  %43 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %62, <4 x i32> %61)
  %44 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %49, <4 x i32> %55, <4 x i32> %61)
  %45 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %65, i64 0))
  %46 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %65, i32 %64, <4 x i32> %60)
  %47 = add <4 x i32> %67, <4 x i32> %K2
  %48 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %68, <4 x i32> %67)
  %49 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %55, <4 x i32> %61, <4 x i32> %67)
  %50 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %46, i64 0))
  %51 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %46, i32 %45, <4 x i32> %66)
  %52 = add <4 x i32> %48, <4 x i32> %K2
  %53 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %49, <4 x i32> %48)
  %54 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %61, <4 x i32> %43, <4 x i32> %48)
  %55 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %51, i64 0))
  %56 = call <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %51, i32 %50, <4 x i32> %47)
  %57 = add <4 x i32> %53, <4 x i32> %K2
  %58 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %54, <4 x i32> %53)
  %59 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %43, <4 x i32> %48, <4 x i32> %53)
  %60 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %56, i64 0))
  %61 = call <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %56, i32 %55, <4 x i32> %52)
  %62 = add <4 x i32> %58, <4 x i32> %K2
  %63 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %59, <4 x i32> %58)
  %64 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %48, <4 x i32> %53, <4 x i32> %58)
  %65 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %61, i64 0))
  %66 = call <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %61, i32 %60, <4 x i32> %57)
  %67 = add <4 x i32> %63, <4 x i32> %K2
  %68 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %64, <4 x i32> %63)
  %69 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %53, <4 x i32> %58, <4 x i32> %63)
  %70 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %66, i64 0))
  %71 = call <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %66, i32 %65, <4 x i32> %62)
  %72 = add <4 x i32> %68, <4 x i32> %K3
  %73 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %69, <4 x i32> %68)
  %74 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %58, <4 x i32> %63, <4 x i32> %68)
  %75 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %71, i64 0))
  %76 = call <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %71, i32 %70, <4 x i32> %67)
  %77 = add <4 x i32> %73, <4 x i32> %K3
  %78 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %74, <4 x i32> %73)
  %79 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %63, <4 x i32> %68, <4 x i32> %73)
  %80 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %76, i64 0))
  %81 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %76, i32 %75, <4 x i32> %72)
  %82 = add <4 x i32> %78, <4 x i32> %K3
  %83 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %79, <4 x i32> %78)
  %84 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %68, <4 x i32> %73, <4 x i32> %78)
  %85 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %81, i64 0))
  %86 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %81, i32 %80, <4 x i32> %77)
  %87 = add <4 x i32> %83, <4 x i32> %K3
  %88 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %84, <4 x i32> %83)
  %89 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %86, i64 0))
  %90 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %86, i32 %85, <4 x i32> %82)
  %91 = add <4 x i32> %88, <4 x i32> %K3
  %92 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %90, i64 0))
  %93 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %90, i32 %89, <4 x i32> %87)
  %94 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %93, i64 0))
  %95 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %93, i32 %92, <4 x i32> %91)
  %96 = add <4 x i32> %95, %buf
  %97 = add i32 %94, %sz
  %98 = insertelement <4 x i32> <i32 poison, i32 0, i32 0, i32 0>, i32 %97, i64 0
  %99 = insertvalue %struct.uint32x4x2_t poison, <4 x i32> %96, 0, 0
  %100 = insertvalue %struct.uint32x4x2_t %99, <4 x i32> %98, 0, 1
  ret %struct.uint32x4x2_t %100
}

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(none)
declare i32 @llvm.aarch64.crypto.sha1h(i32) #1

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(none)
declare <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32>, i32, <4 x i32>) #1

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(none)
declare <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32>, <4 x i32>, <4 x i32>) #1

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(none)
declare <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32>, <4 x i32>) #1

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(none)
declare <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32>, i32, <4 x i32>) #1

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(none)
declare <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32>, i32, <4 x i32>) #1

attributes #0 = { mustprogress nofree noinline norecurse nosync nounwind ssp willreturn memory(none) "frame-pointer"="non-leaf" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="apple-a14" "target-features"="+aes,+altnzcv,+ccdp,+ccidx,+complxnum,+crc,+dit,+dotprod,+flagm,+fp-armv8,+fp16fml,+fptoint,+fullfp16,+jsconv,+lse,+neon,+pauth,+perfmon,+predres,+ras,+rcpc,+rdm,+sb,+sha2,+sha3,+specrestrict,+ssbs,+v8.1a,+v8.2a,+v8.3a,+v8.4a,+v8a,+zcm,+zcz" }
attributes #1 = { nocallback nofree nosync nounwind willreturn memory(none) }

!llvm.linker.options = !{}
!llvm.module.flags = !{!0, !1, !2}
!llvm.ident = !{!3}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 8, !"PIC Level", i32 2}
!2 = !{i32 7, !"frame-pointer", i32 1}
!3 = !{!"Homebrew clang version 19.1.5"}
